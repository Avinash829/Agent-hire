"""
Text Utility Functions.

Provides helper functions for text processing, truncation,
and formatting used across the application.
"""

from typing import Optional


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
    import re
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

