"""
LangGraph Web Reputation Investigation Node.

Replaces the previous Reddit-based investigation with a Tavily Search
powered web reputation investigation. Maintains the same output schema
for backward compatibility with the LangGraph workflow.
"""

from typing import Optional, Dict, Any
from app.state.agent_state import AgentState
from app.config.settings import get_settings
from app.agents.common.reputation_constants import (
    REPUTATION_ANALYSIS_PROMPT,
)
from app.agents.common.tavily_utils import (
    generate_search_query,
    call_tavily,
    filter_results,
    prepare_llm_context,
)
from app.agents.common.gemini_analyzer import (
    analyze_reputation,
    build_reputation_response,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)


def investigate_web_reputation(state: AgentState) -> AgentState:
    """
    Investigate company reputation using Tavily Search.

    Performs a single optimized web search and analyzes results
    with Gemini to determine hiring legitimacy and reputation.

    Args:
        state: Current agent state.

    Returns:
        AgentState: State with web reputation investigation data.
    """
    logger.info("[Online Reputation] Started")

    updated_state = dict(state)
    company_name = state.get("company_name", "")
    company_domain = state.get("company_domain", "")

    reddit_data = {
        "mentions_count": 0,
        "scam_mentions": 0,
        "positive_mentions": 0,
        "sentiment": "neutral",
        "top_posts": [],
        "status": "pending",
    }

    if not company_name and not company_domain:
        logger.warning("[Online Reputation] No company info available")
        reddit_data["status"] = "skipped"
        reddit_data["error"] = "No company name or domain available"
        updated_state["reddit_data"] = reddit_data
        logger.info("[Online Reputation] Completed (skipped)")
        return updated_state

    try:
        settings = get_settings()
        tavily_api_key = settings.tavily_api_key
        gemini_api_key = settings.gemini_api_key

        if not tavily_api_key:
            logger.error("[Online Reputation] TAVILY_API_KEY is not configured")
            reddit_data["status"] = "error"
            reddit_data["error"] = "Tavily API key not configured"
            updated_state["reddit_data"] = reddit_data
            logger.info("[Online Reputation] Completed (no API key)")
            return updated_state

        # Step 1: Generate optimized search query
        query = generate_search_query(company_name, company_domain)

        # Step 2: Execute single Tavily search
        logger.info("[Tavily] Sending request...")
        response = call_tavily(query, tavily_api_key)

        if not response:
            logger.warning("[Online Reputation] Tavily search returned no response")
            reddit_data["status"] = "completed"
            reddit_data["sentiment"] = "neutral"
            reddit_data["error"] = "No search results available"
            updated_state["reddit_data"] = reddit_data
            logger.info("[Online Reputation] Completed (no results)")
            return updated_state

        logger.info("[Tavily] Response received")

        # Step 3: Filter and clean results
        raw_results = response.get("results", [])
        filtered_results = filter_results(raw_results)
        answer = response.get("answer")

        if not filtered_results:
            logger.warning("[Online Reputation] No relevant results after filtering")
            reddit_data["status"] = "completed"
            reddit_data["sentiment"] = "neutral"
            reddit_data["error"] = "No relevant search results found"
            updated_state["reddit_data"] = reddit_data
            logger.info("[Online Reputation] Completed (no relevant results)")
            return updated_state

        # Step 4: Prepare context for LLM
        search_context = prepare_llm_context(filtered_results, answer)

        # Step 5: Analyze with Gemini
        analysis = analyze_reputation(
            company_name=company_name,
            company_domain=company_domain,
            search_context=search_context,
            api_key=gemini_api_key,
            prompt_template=REPUTATION_ANALYSIS_PROMPT,
        )

        # Step 6: Build response
        reddit_data = build_reputation_response(analysis, len(filtered_results))
        reddit_data["status"] = "completed"

        logger.info(
            "[Online Reputation] Completed: %d mentions, sentiment=%s, risk_score=%s",
            reddit_data["mentions_count"],
            reddit_data["sentiment"],
            reddit_data.get("risk_score", "N/A"),
        )

    except Exception as exception:
        logger.exception("[Online Reputation] Failed: %s", str(exception))
        reddit_data["status"] = "failed"
        reddit_data["error"] = str(exception)

    updated_state["reddit_data"] = reddit_data
    return updated_state


__all__ = ["investigate_web_reputation"]
