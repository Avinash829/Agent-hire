"""
Text Utility Functions.

Provides helper functions for text processing, truncation,
JSON parsing, and formatting used across the application.
"""

import json
import re
from typing import Optional, Any, Dict


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a specified maximum length with a suffix.

    Args:
        text: The text to truncate.
        max_length: Maximum number of characters.
        suffix: String to append when truncated.

    Returns:
        str: The truncated text.
    """
    if len(text) <= max_length:
        return text

    truncated = text[: max_length - len(suffix)].strip()
    return f"{truncated}{suffix}"


def extract_company_name_from_url(url: str) -> Optional[str]:
    """
    Attempt to extract a company name from a URL domain.

    Args:
        url: The URL to extract from.

    Returns:
        Optional[str]: The extracted company name, or None.
    """
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        domain = domain.replace("www.", "")

        parts = domain.split(".")
        if len(parts) >= 2:
            return parts[0].capitalize()

        return None
    except Exception:
        return None


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace by collapsing multiple spaces into one.

    Args:
        text: The text to normalize.

    Returns:
        str: The normalized text.
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def parse_json_response(content: Any) -> Optional[Dict[str, Any]]:
    """
    Safely parse a JSON response from an LLM, handling markdown fences
    and LangChain's list-based multimodal message format.

    Strips ```json, ```, and leading/trailing whitespace before parsing.
    Returns None if parsing fails, with no exception raised.

    Args:
        content: Raw response string or list from an LLM.

    Returns:
        Optional[Dict]: Parsed JSON dictionary, or None if unparseable.
    """
    if not content:
        return None

    # Handle LangChain's newer list-based message format
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
            elif isinstance(part, str):
                text_parts.append(part)
        content = "".join(text_parts)
    elif not isinstance(content, str):
        # Fallback to string casting just in case
        content = str(content)

    cleaned = content.strip()

    # Remove ```json prefix
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    # Remove ``` suffix
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    if not cleaned:
        return None

    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        return None