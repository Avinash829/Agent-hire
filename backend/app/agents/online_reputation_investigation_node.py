"""
LangGraph Online Reputation Investigation Node.

Performs web reputation analysis using Tavily Search and Gemini
to assess a company's hiring legitimacy and online presence.
"""

from typing import Optional, Dict, Any, List
import json
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from app.state.agent_state import AgentState
from app.config.settings import get_settings
from app.constants.agent_constants import (
    TAVILY_MAX_RESULTS,
    TAVILY_SEARCH_DEPTH,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)

# Keywords for reputation analysis
SCAM_KEYWORDS: List[str] = [
    "scam", "fraud", "fake", "phishing", "avoid", "warning",
    "illegitimate", "cheating", "dishonest", "untrustworthy",
]

POSITIVE_KEYWORDS: List[str] = [
    "legitimate", "trusted", "recommended", "great", "good",
    "professional", "reliable", "reputable", "established",
]

REPUTATION_ANALYSIS_PROMPT: str = """
You are a fraud detection expert analyzing online reputation data for a company.

Company Name: {company_name}
Company Domain: {company_domain}

Web Search Results:
{search_context}

Analyze the search results and determine:

1. Is this company legitimate?
2. Are hiring scams or recruitment fraud reported?
3. Are fake interviews or phishing attempts reported?
4. Is there evidence of genuine hiring and trusted company presence?
5. What is the overall online reputation?

Respond with a JSON object:
{{
    "risk_score": <float between 0 and 1>,
    "overall_sentiment": "Mostly Positive" | "Mixed" | "Mostly Negative" | "Neutral",
    "legitimate_presence": true | false,
    "scam_reports_found": true | false,
    "confidence": <float between 0 and 1>,
    "summary": "<one or two sentence summary>",
    "reasoning": "<detailed analysis reasoning>",
    "key_findings": ["<list of key findings>"],
    "positive_sources": ["<list of positive source descriptions>"],
    "negative_sources": ["<list of negative source descriptions>"]
}}

Be conservative. Only flag as high risk if there is strong evidence.
Base your analysis ONLY on the provided search results.
"""


def _generate_search_query(company_name: str, domain: Optional[str] = None) -> str:
    """
    Generate a single optimized Tavily search query.

    Combines company identifiers with reputation-related terms
    to maximise relevant results in one request.

    Args:
        company_name: Name of the company to investigate.
        domain: Optional company domain.

    Returns:
        str: Optimized search query string.
    """
    company_identifier = company_name
    if domain and domain not in company_name.lower():
        company_identifier = f"{company_name} ({domain})"

    query = (
        f"{company_identifier} hiring scam OR recruitment fraud "
        f"OR fake jobs OR company reviews OR employee experiences"
    )
    logger.debug(f"Generated search query: {query}")
    return query


def _call_tavily(query: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Execute a single Tavily search API call.

    Uses conservative settings to minimise credit consumption.

    Args:
        query: Search query string.
        api_key: Tavily API key.

    Returns:
        Optional[Dict]: Tavily response or None on failure.
    """
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            search_depth=TAVILY_SEARCH_DEPTH,
            max_results=TAVILY_MAX_RESULTS,
            include_answer=True,
            include_images=False,
            include_raw_content=False,
        )
        logger.info(
            f"Tavily search completed: {len(response.get('results', []))} results"
        )
        return response
    except Exception as exception:
        logger.error(f"Tavily search failed: {exception}")
        return None


def _filter_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate and irrelevant results from Tavily response.

    Deduplicates by URL and filters out clearly irrelevant content.

    Args:
        results: Raw list of result dictionaries from Tavily.

    Returns:
        List[Dict]: Cleaned and deduplicated results.
    """
    seen_urls: set = set()
    filtered: List[Dict[str, Any]] = []

    for result in results:
        url = result.get("url", "")
        title = result.get("title", "")
        content = result.get("content", "")

        if not url or url in seen_urls:
            continue

        if not title and not content:
            continue

        seen_urls.add(url)
        filtered.append(result)

    logger.debug(f"Filtered results: {len(filtered)} from {len(results)} total")
    return filtered


def _prepare_llm_context(
    results: List[Dict[str, Any]],
    answer: Optional[str] = None,
) -> str:
    """
    Prepare a concise context string from search results for LLM analysis.

    Extracts only essential information: title, content summary, and source.

    Args:
        results: Filtered search results.
        answer: Optional Tavily generated answer.

    Returns:
        str: Concise context string for LLM prompt.
    """
    context_parts: List[str] = []

    if answer:
        context_parts.append(f"Summary Answer: {answer}\n")

    for i, result in enumerate(results, 1):
        title = result.get("title", "Untitled")
        content = result.get("content", "")
        url = result.get("url", "")

        content_preview = content[:300] if content else "No content available"
        context_parts.append(
            f"Result {i}:\n"
            f"Title: {title}\n"
            f"Content: {content_preview}\n"
            f"Source: {url}\n"
        )

    return "\n".join(context_parts)


def _analyze_reputation(
    company_name: str,
    company_domain: Optional[str],
    search_context: str,
    api_key: str,
) -> Dict[str, Any]:
    """
    Send cleaned search context to Gemini for reputation analysis.

    Args:
        company_name: Name of the company.
        company_domain: Optional company domain.
        search_context: Prepared context string from search results.
        api_key: Gemini API key.

    Returns:
        Dict: Structured reputation analysis result.
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.2,
        )

        prompt = REPUTATION_ANALYSIS_PROMPT.format(
            company_name=company_name or "Unknown",
            company_domain=company_domain or "Unknown",
            search_context=search_context,
        )

        messages = [
            SystemMessage(
                content="You are a fraud detection expert. Analyze web reputation "
                "data and return structured JSON assessments."
            ),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)
        content = response.content.strip()

        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]

        analysis = json.loads(content)
        logger.info("Gemini reputation analysis completed successfully")
        return analysis

    except json.JSONDecodeError as json_error:
        logger.error(f"Failed to parse Gemini response: {json_error}")
        return _get_fallback_analysis("Failed to parse AI analysis")
    except Exception as exception:
        logger.error(f"Gemini reputation analysis failed: {exception}")
        return _get_fallback_analysis(str(exception))


def _get_fallback_analysis(error_message: str) -> Dict[str, Any]:
    """
    Return a safe fallback analysis when Gemini analysis fails.

    Args:
        error_message: Description of the error.

    Returns:
        Dict: Safe fallback analysis result.
    """
    return {
        "risk_score": 0.5,
        "overall_sentiment": "Neutral",
        "legitimate_presence": False,
        "scam_reports_found": False,
        "confidence": 0.0,
        "summary": f"Reputation analysis unavailable: {error_message}",
        "reasoning": "Analysis could not be completed due to an error.",
        "key_findings": [],
        "positive_sources": [],
        "negative_sources": [],
    }


def _build_response(
    analysis: Dict[str, Any],
    results_count: int,
) -> Dict[str, Any]:
    """
    Build the structured response for downstream consumers.

    Maps Tavily/Gemini analysis fields to the expected output format.

    Args:
        analysis: Reputation analysis from Gemini.
        results_count: Number of search results found.

    Returns:
        Dict: Structured response with reputation analysis data.
    """
    scam_mentions = 0
    positive_mentions = 0

    if analysis.get("scam_reports_found"):
        scam_mentions = max(1, results_count // 2)

    if analysis.get("legitimate_presence"):
        positive_mentions = max(1, results_count // 3)

    sentiment = analysis.get("overall_sentiment", "Neutral").lower()

    top_posts = []
    for source in analysis.get("negative_sources", []):
        top_posts.append({
            "title": source,
            "score": -1,
            "source_type": "web",
            "sentiment": "negative",
        })
    for source in analysis.get("positive_sources", []):
        top_posts.append({
            "title": source,
            "score": 1,
            "source_type": "web",
            "sentiment": "positive",
        })

    return {
        "mentions_count": results_count,
        "scam_mentions": scam_mentions,
        "positive_mentions": positive_mentions,
        "sentiment": sentiment,
        "top_posts": top_posts[:5],
        "status": "completed",
        "risk_score": analysis.get("risk_score", 0.5),
        "overall_sentiment": analysis.get("overall_sentiment", "Neutral"),
        "legitimate_presence": analysis.get("legitimate_presence", False),
        "scam_reports_found": analysis.get("scam_reports_found", False),
        "confidence": analysis.get("confidence", 0.0),
        "summary": analysis.get("summary", ""),
        "reasoning": analysis.get("reasoning", ""),
        "key_findings": analysis.get("key_findings", []),
    }


def investigate_online_reputation(state: AgentState) -> AgentState:
    """
    Investigate company reputation using Tavily Search.

    Performs a single optimized web search and analyzes results
    with Gemini to determine hiring legitimacy and reputation.

    Args:
        state: Current agent state.

    Returns:
        AgentState: State with online reputation investigation data.
    """
    logger.info("Starting online reputation investigation via Tavily")

    updated_state = dict(state)
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
        logger.warning("No company info available for online reputation search")
        online_reputation_data["status"] = "skipped"
        online_reputation_data["error"] = "No company name or domain available"
        updated_state["online_reputation_data"] = online_reputation_data
        return updated_state

    try:
        settings = get_settings()
        tavily_api_key = settings.tavily_api_key
        gemini_api_key = settings.gemini_api_key

        if not tavily_api_key:
            logger.error("TAVILY_API_KEY is not configured")
            online_reputation_data["status"] = "error"
            online_reputation_data["error"] = "Tavily API key not configured"
            updated_state["online_reputation_data"] = online_reputation_data
            return updated_state

        # Step 1: Generate optimized search query
        logger.info("Generating optimized search query")
        query = _generate_search_query(company_name, company_domain)

        # Step 2: Execute single Tavily search
        logger.info(f"Calling Tavily search: {query}")
        response = _call_tavily(query, tavily_api_key)

        if not response:
            logger.warning("Tavily search returned no response")
            online_reputation_data["status"] = "completed"
            online_reputation_data["sentiment"] = "neutral"
            online_reputation_data["error"] = "No search results available"
            updated_state["online_reputation_data"] = online_reputation_data
            return updated_state

        # Step 3: Filter and clean results
        raw_results = response.get("results", [])
        filtered_results = _filter_results(raw_results)
        answer = response.get("answer")

        logger.info(
            f"Tavily search: {len(filtered_results)} relevant results "
            f"from {len(raw_results)} raw results"
        )

        if not filtered_results:
            logger.warning("No relevant results after filtering")
            online_reputation_data["status"] = "completed"
            online_reputation_data["sentiment"] = "neutral"
            online_reputation_data["error"] = "No relevant search results found"
            updated_state["online_reputation_data"] = online_reputation_data
            return updated_state

        # Step 4: Prepare context for LLM
        logger.info("Preparing context for Gemini analysis")
        search_context = _prepare_llm_context(filtered_results, answer)

        # Step 5: Analyze with Gemini
        logger.info("Calling Gemini for reputation analysis")
        analysis = _analyze_reputation(
            company_name=company_name,
            company_domain=company_domain,
            search_context=search_context,
            api_key=gemini_api_key,
        )

        # Step 6: Build response
        online_reputation_data = _build_response(analysis, len(filtered_results))
        online_reputation_data["status"] = "completed"

        logger.info(
            f"Online reputation investigation completed: "
            f"{online_reputation_data['mentions_count']} mentions found, "
            f"sentiment={online_reputation_data['sentiment']}, "
            f"risk_score={online_reputation_data.get('risk_score', 'N/A')}"
        )

    except Exception as exception:
        logger.warning(f"Online reputation investigation failed: {exception}")
        online_reputation_data["status"] = "failed"
        online_reputation_data["error"] = str(exception)

    updated_state["online_reputation_data"] = online_reputation_data
    return updated_state


__all__ = ["investigate_online_reputation"]

