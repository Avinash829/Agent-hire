"""
LangGraph Company Extraction Node.

Extracts company name and domain from the job description
using Gemini LLM or heuristic methods.
"""

import json
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from app.state.agent_state import AgentState
from app.config.settings import get_settings
from app.prompts.gemini_prompts import COMPANY_EXTRACTION_PROMPT
from app.utils.url_utils import extract_domain, sanitize_url
from app.logging.logger import get_logger

logger = get_logger(__name__)


def extract_company(state: AgentState) -> AgentState:
    """
    Extract company information from the job description.

    Uses Gemini LLM for extraction, with heuristic fallback.

    Args:
        state: Current agent state.

    Returns:
        AgentState: State with extracted company information.
    """
    logger.info("Extracting company information from job description")

    updated_state = dict(state)
    job_description = state.get("job_description", "")
    source_link = state.get("source_link", "")

    company_name = None
    company_domain = None

    try:
        settings = get_settings()
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.gemini_api_key,
            temperature=0.1,
        )

        prompt = COMPANY_EXTRACTION_PROMPT.format(
            job_description=job_description[:2000]
        )

        response = llm.invoke(prompt)
        content = response.content.strip()

        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]

        extracted = json.loads(content)
        company_name = extracted.get("company_name")

        mentioned_urls = extracted.get("mentioned_urls", [])
        if mentioned_urls:
            for url in mentioned_urls:
                domain = extract_domain(url)
                if domain:
                    company_domain = domain
                    break

    except Exception as exception:
        logger.warning(f"LLM extraction failed: {exception}. Using heuristic fallback.")

    if not company_name and source_link:
        from app.utils.text_utils import extract_company_name_from_url
        company_name = extract_company_name_from_url(source_link)

    if not company_domain and source_link:
        company_domain = extract_domain(source_link)

    if company_name:
        updated_state["company_name"] = company_name
    if company_domain:
        updated_state["company_domain"] = company_domain

    logger.info(
        f"Company extraction: name={company_name}, domain={company_domain}"
    )
    return updated_state

