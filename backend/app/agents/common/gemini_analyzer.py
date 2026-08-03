"""
Shared Gemini reputation analysis utilities.

Provides common functions for sending reputation context to Gemini
and building structured responses for downstream consumers.
"""

from typing import Optional, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from app.utils.text_utils import parse_json_response
from app.logging.logger import get_logger
from app.agents.common.llm_factory import get_gemini_llm_with_fallbacks

logger = get_logger(__name__)


def analyze_reputation(
    company_name: str,
    company_domain: Optional[str],
    search_context: str,
    api_key: str,
    prompt_template: str,
) -> Dict[str, Any]:
    """
    Send cleaned search context to Gemini for reputation analysis.

    Args:
        company_name: Name of the company.
        company_domain: Optional company domain.
        search_context: Prepared context string from search results.
        api_key: Gemini API key.
        prompt_template: The prompt template with {company_name}, {company_domain}, {search_context}.

    Returns:
        Dict: Structured reputation analysis result.
    """
    try:
        logger.info("[Gemini] Sending reputation analysis request...")
        llm = get_gemini_llm_with_fallbacks(temperature=0.1)

        prompt = prompt_template.format(
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
        analysis = parse_json_response(response.content)

        if analysis:
            logger.info("[Gemini] Reputation analysis response received")
            return analysis

        logger.warning("[Gemini] Could not parse reputation analysis JSON, using fallback")
        return _get_fallback_analysis("Failed to parse AI analysis")

    except Exception as exception:
        logger.exception("[Gemini] Reputation analysis failed: %s", str(exception))
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


def build_reputation_response(
    analysis: Dict[str, Any],
    results_count: int,
    source_type: str = "web",
) -> Dict[str, Any]:
    """
    Build the structured response for downstream consumers.

    Uses real lengths from extracted evidence arrays instead of
    synthetic multipliers.

    Args:
        analysis: Reputation analysis from Gemini.
        results_count: Number of search results found.
        source_type: Type of source ('web' or 'reddit').

    Returns:
        Dict: Structured response with reputation analysis data.
    """
    scam_mentions = 0
    positive_mentions = 0

    negative_sources = analysis.get("negative_sources", [])
    positive_sources = analysis.get("positive_sources", [])

    if analysis.get("scam_reports_found"):
        scam_mentions = len(negative_sources)

    if analysis.get("legitimate_presence"):
        positive_mentions = len(positive_sources)

    sentiment = analysis.get("overall_sentiment", "Neutral").lower()

    top_posts = []
    for source in negative_sources:
        top_posts.append({
            "title": source,
            "score": -1,
            "source_type": source_type,
            "sentiment": "negative",
        })
    for source in positive_sources:
        top_posts.append({
            "title": source,
            "score": 1,
            "source_type": source_type,
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
