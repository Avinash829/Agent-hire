"""
LangGraph Online Reputation Investigation Node.

Performs web reputation analysis using Tavily Search and Gemini
to assess a company's hiring legitimacy and online presence.
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


def investigate_online_reputation(state: AgentState) -> dict:
    """
    Investigate company reputation using Tavily Search.
    """
    logger.info("[Online Reputation] Started")

    company_name = state.get("company_name", "")
    company_domain = state.get("company_domain", "")

    online_reputation_data = {
        "mentions_count": 0,
        "scam_mentions": 0,
        "positive_mentions": 0,
        "sentiment": "neutral",
        "top_posts": [],
        "status": "pending",
    }

    if not company_name and not company_domain:
        logger.warning("[Online Reputation] No company info available")
        online_reputation_data["status"] = "skipped"
        online_reputation_data["error"] = "No company name or domain available"
        logger.info("[Online Reputation] Completed (skipped)")
        return {"online_reputation_data": online_reputation_data}

    try:
        settings = get_settings()
        tavily_api_key = settings.tavily_api_key
        gemini_api_key = settings.gemini_api_key

        if not tavily_api_key:
            logger.error("[Online Reputation] TAVILY_API_KEY is not configured")
            online_reputation_data["status"] = "error"
            online_reputation_data["error"] = "Tavily API key not configured"
            logger.info("[Online Reputation] Completed (no API key)")
            return {"online_reputation_data": online_reputation_data}

        # Step 1: Generate optimized search query
        query = generate_search_query(company_name, company_domain)

        # Step 2: Execute single Tavily search
        logger.info("[Tavily] Sending request...")
        response = call_tavily(query, tavily_api_key)

        if not response:
            logger.warning("[Online Reputation] Tavily search returned no response")
            online_reputation_data["status"] = "completed"
            online_reputation_data["sentiment"] = "neutral"
            online_reputation_data["error"] = "No search results available"
            logger.info("[Online Reputation] Completed (no results)")
            return {"online_reputation_data": online_reputation_data}

        logger.info("[Tavily] Response received")

        # Step 3: Filter and clean results
        raw_results = response.get("results", [])
        filtered_results = filter_results(raw_results)
        answer = response.get("answer")

        if not filtered_results:
            logger.warning("[Online Reputation] No relevant results after filtering")
            online_reputation_data["status"] = "completed"
            online_reputation_data["sentiment"] = "neutral"
            online_reputation_data["error"] = "No relevant search results found"
            logger.info("[Online Reputation] Completed (no relevant results)")
            return {"online_reputation_data": online_reputation_data}

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
        online_reputation_data = build_reputation_response(analysis, len(filtered_results))
        online_reputation_data["status"] = "completed"

        logger.info(
            "[Online Reputation] Completed: %d mentions, sentiment=%s, risk_score=%s",
            online_reputation_data["mentions_count"],
            online_reputation_data["sentiment"],
            online_reputation_data.get("risk_score", "N/A"),
        )

        return {"online_reputation_data": online_reputation_data}

    except Exception as exception:
        logger.exception("[Online Reputation] Failed: %s", str(exception))
        online_reputation_data["status"] = "failed"
        online_reputation_data["error"] = str(exception)
        
        return {
            "online_reputation_data": online_reputation_data,
            "errors": [f"Online reputation investigation failed: {str(exception)[:200]}"]
        }


__all__ = ["investigate_online_reputation"]