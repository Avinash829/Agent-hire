"""
LangGraph Website Investigation Node.

Scrapes the company website to verify career page existence,
job posting legitimacy, and overall website quality.
"""

import httpx
from selectolax.parser import HTMLParser
from app.state.agent_state import AgentState
from app.constants.agent_constants import (
    REQUEST_TIMEOUT_SECONDS,
    MAX_REDIRECT_FOLLOWS,
    CAREER_PAGE_KEYWORDS,
)
from app.logging.logger import get_logger
from app.constants.ats_constants import (
    is_trusted_ats_domain,
    get_ats_provider,
)
from app.utils.url_utils import extract_domain, extract_ats_provider

logger = get_logger(__name__)


def _detect_ats(state: AgentState):
    """Detect a trusted ATS provider from links or domain."""
    source_link = state.get("source_link", "")
    application_link = state.get("application_link", "")
    domain = state.get("company_domain", "")

    for candidate in (application_link, source_link, domain or ""):
        if not candidate:
            continue
        provider = None
        if candidate.startswith("http"):
            provider = extract_ats_provider(candidate)
        elif is_trusted_ats_domain(candidate):
            provider = get_ats_provider(candidate)
        if provider:
            return candidate, provider
    return None, None


async def investigate_website(state: AgentState) -> dict:
    """
    Investigate the company website for career page and legitimacy signals.

    Detects trusted ATS/job board providers from source and application
    links first, bypassing root-domain crawling when a provider is found.
    """
    logger.info("[Website Investigation] Started")

    domain = state.get("company_domain")
    ats_url, ats_provider = _detect_ats(state)

    if not domain and not ats_url:
        logger.warning("[Website Investigation] No domain available")
        logger.info("[Website Investigation] Completed (no domain)")
        return {"website_data": {"error": "No domain available"}}

    website_data = {
        "domain": domain,
        "has_career_page": False,
        "ats_provider_detected": bool(ats_url),
        "ats_provider": ats_provider,
        "career_page_url": ats_url,
        "page_title": None,
        "redirect_count": 0,
        "status": "pending",
    }

    if ats_url:
        website_data["has_career_page"] = True
        website_data["status"] = "completed"
        logger.info(
            "[Website Investigation] ATS provider detected: %s",
            ats_provider,
        )
        return {"website_data": website_data}

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            max_redirects=MAX_REDIRECT_FOLLOWS,
        ) as client:
            base_url = f"https://{domain}"
            try:
                response = await client.get(base_url)
                website_data["status_code"] = response.status_code
                website_data["redirect_count"] = len(response.history)

                if response.status_code == 200:
                    parser = HTMLParser(response.text)
                    title_tag = parser.css_first("title")
                    if title_tag:
                        website_data["page_title"] = title_tag.text().strip()

                    for keyword in CAREER_PAGE_KEYWORDS:
                        career_url = f"{base_url}/{keyword.replace(' ', '-')}"
                        try:
                            career_response = await client.get(career_url)
                            if career_response.status_code == 200:
                                website_data["has_career_page"] = True
                                website_data["career_page_url"] = career_url
                                break
                        except Exception:
                            continue

                    text_content = response.text.lower()
                    if any(k in text_content for k in CAREER_PAGE_KEYWORDS):
                        website_data["has_career_page"] = True

                    website_data["status"] = "completed"

            except httpx.TimeoutException:
                logger.warning("[Website Investigation] Timeout fetching %s", base_url)
                website_data["status"] = "timeout"
            except httpx.RequestError as request_error:
                logger.warning("[Website Investigation] Request error for %s: %s", base_url, request_error)
                website_data["status"] = "error"
                website_data["error"] = str(request_error)

        logger.info(
            "[Website Investigation] Completed: has_career_page=%s",
            website_data["has_career_page"],
        )
        return {"website_data": website_data}

    except Exception as exception:
        logger.exception("[Website Investigation] Failed: %s", str(exception))
        website_data["status"] = "failed"
        website_data["error"] = str(exception)

        return {
            "website_data": website_data,
            "errors": [f"Website investigation failed: {str(exception)[:200]}"],
        }
