"""
LangGraph Website Investigation Node.

Scrapes the company website to verify career page existence,
job posting legitimacy, and overall website quality.
"""

from typing import Optional, Dict, Any
import httpx
from selectolax.parser import HTMLParser
from app.state.agent_state import AgentState
from app.constants.agent_constants import (
    REQUEST_TIMEOUT_SECONDS,
    MAX_REDIRECT_FOLLOWS,
    CAREER_PAGE_KEYWORDS,
    URL_FETCH_TIMEOUT,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)


async def investigate_website(state: AgentState) -> AgentState:
    """
    Investigate the company website for career page and legitimacy signals.

    Checks:
    - Career page existence
    - Page content quality
    - Redirect chains

    Args:
        state: Current agent state.

    Returns:
        AgentState: State with website investigation data.
    """
    logger.info("Starting website investigation")

    updated_state = dict(state)
    domain = state.get("company_domain")

    if not domain:
        logger.warning("No domain available for website investigation")
        updated_state["website_data"] = {"error": "No domain available"}
        return updated_state

    website_data = {
        "domain": domain,
        "has_career_page": False,
        "career_page_url": None,
        "page_title": None,
        "redirect_count": 0,
        "status": "pending",
    }

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

                    meta_tags = parser.css("meta[name='description']")
                    if meta_tags:
                        website_data["meta_description"] = (
                            meta_tags[0].attributes.get("content", "")
                        )

                    for keyword in CAREER_PAGE_KEYWORDS:
                        career_url = f"{base_url}/{keyword.replace(' ', '-')}"
                        try:
                            career_response = await client.get(career_url)
                            if career_response.status_code == 200:
                                website_data["has_career_page"] = True
                                website_data["career_page_url"] = career_url
                                website_data["career_page_status"] = (
                                    career_response.status_code
                                )
                                break
                        except Exception:
                            continue

                    text_content = response.text.lower()
                    for keyword in CAREER_PAGE_KEYWORDS:
                        if keyword in text_content:
                            website_data["has_career_page"] = True
                            break

                    website_data["status"] = "completed"

            except httpx.TimeoutException:
                logger.warning(f"Timeout fetching {base_url}")
                website_data["status"] = "timeout"
            except httpx.RequestError as request_error:
                logger.warning(f"Request error for {base_url}: {request_error}")
                website_data["status"] = "error"
                website_data["error"] = str(request_error)

    except Exception as exception:
        logger.warning(f"Website investigation failed: {exception}")
        website_data["status"] = "failed"
        website_data["error"] = str(exception)

    updated_state["website_data"] = website_data
    logger.info(
        f"Website investigation completed: "
        f"has_career_page={website_data['has_career_page']}"
    )
    return updated_state

