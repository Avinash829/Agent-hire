"""
Shared Tavily search utilities.

Provides common functions for executing Tavily searches,
filtering results, and preparing LLM context.
"""

from typing import Optional, Dict, Any, List
from tavily import TavilyClient
from app.constants.agent_constants import (
    TAVILY_MAX_RESULTS,
    TAVILY_SEARCH_DEPTH,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)


def generate_search_query(company_name: str, domain: Optional[str] = None) -> str:
    """
    Generate a balanced Tavily search query.

    Gathers corporate identity signals (headcount, headquarters, LinkedIn
    presence) alongside risk checks to prevent confirmation bias.

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
        f"{company_identifier} company overview headcount headquarters "
        f"LinkedIn presence careers and reviews"
    )
    logger.debug("[Tavily] Generated search query: %s", query)
    return query


def call_tavily(query: str, api_key: str) -> Optional[Dict[str, Any]]:
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
        logger.info("[Tavily] Sending request...")
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
            "[Tavily] Response received: %d results",
            len(response.get("results", [])),
        )
        return response
    except Exception as exception:
        logger.exception("[Tavily] Failed: %s", str(exception))
        return None


def filter_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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

    logger.debug("[Tavily] Filtered results: %d from %d total", len(filtered), len(results))
    return filtered


def prepare_llm_context(
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

