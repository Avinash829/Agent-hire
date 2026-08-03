"""
LangGraph Evidence Aggregation Node.

Collects and structures evidence from all investigation nodes
for Gemini reasoning and final report generation.
"""

from typing import Dict, Any
from app.state.agent_state import AgentState
from app.logging.logger import get_logger

logger = get_logger(__name__)


def aggregate_evidence(state: AgentState) -> AgentState:
    """
    Aggregate evidence from all investigation sources.

    Combines WHOIS, website, and web reputation investigation data
    into a structured evidence object.

    Args:
        state: Current agent state.

    Returns:
        AgentState: State with aggregated investigation evidence.
    """
    logger.info("[Evidence Aggregation] Started")

    updated_state = dict(state)
    evidence = {}

    company_name = state.get("company_name", "Unknown")
    company_domain = state.get("company_domain", "Unknown")
    evidence["company_name"] = company_name
    evidence["company_domain"] = company_domain

    whois_data = state.get("whois_data", {})
    if whois_data and whois_data.get("status") == "completed":
        evidence["whois"] = {
            "domain_age_days": whois_data.get("age_days"),
            "registrar": whois_data.get("registrar"),
            "is_suspiciously_young": whois_data.get(
                "is_suspiciously_young", False
            ),
            "creation_date": whois_data.get("creation_date"),
        }
    else:
        evidence["whois"] = {"error": "WHOIS lookup failed or unavailable"}

    website_data = state.get("website_data", {})
    if website_data and website_data.get("status") == "completed":
        evidence["website"] = {
            "has_career_page": website_data.get("has_career_page", False),
            "ats_provider_detected": website_data.get(
                "ats_provider_detected", False
            ),
            "ats_provider": website_data.get("ats_provider"),
            "career_page_url": website_data.get("career_page_url"),
            "page_title": website_data.get("page_title"),
            "status_code": website_data.get("status_code"),
        }
    else:
        evidence["website"] = {
            "error": "Website investigation failed or unavailable"
        }

    online_reputation_data = state.get("online_reputation_data", {})
    if online_reputation_data and online_reputation_data.get("status") == "completed":
        evidence["online_reputation"] = {
            "mentions_count": online_reputation_data.get("mentions_count", 0),
            "scam_mentions": online_reputation_data.get("scam_mentions", 0),
            "positive_mentions": online_reputation_data.get("positive_mentions", 0),
            "sentiment": online_reputation_data.get("sentiment", "neutral"),
            "risk_score": online_reputation_data.get("risk_score", 0.5),
            "overall_sentiment": online_reputation_data.get(
                "overall_sentiment", "Neutral"
            ),
            "legitimate_presence": online_reputation_data.get(
                "legitimate_presence", False
            ),
            "scam_reports_found": online_reputation_data.get(
                "scam_reports_found", False
            ),
            "confidence": online_reputation_data.get("confidence", 0.0),
            "summary": online_reputation_data.get("summary", ""),
            "reasoning": online_reputation_data.get("reasoning", ""),
            "key_findings": online_reputation_data.get("key_findings", []),
            "top_posts": [
                {
                    "title": post.get("title"),
                    "score": post.get("score"),
                    "source_type": post.get("source_type"),
                    "sentiment": post.get("sentiment"),
                }
                for post in online_reputation_data.get("top_posts", [])
            ],
        }
    else:
        evidence["online_reputation"] = {
            "error": "Online reputation investigation failed or unavailable"
        }

    evidence["errors"] = state.get("errors", [])
    updated_state["investigation_evidence"] = evidence

    logger.info("[Evidence Aggregation] Completed")
    return updated_state
