"""
URL Utility Functions.

Provides helper functions for URL parsing, domain extraction,
and URL validation used across the application.
"""

from urllib.parse import urlparse
import re
from typing import Optional
import tldextract
from app.constants.ats_constants import (
    is_trusted_ats_domain,
    get_ats_provider,
)


def extract_domain(url: str) -> Optional[str]:
    """
    Extract the domain name from a URL.

    Args:
        url: The full URL string.

    Returns:
        Optional[str]: The extracted domain, or None if invalid.
    """
    try:
        extracted = tldextract.extract(url)
        if extracted.domain and extracted.suffix:
            return f"{extracted.domain}.{extracted.suffix}"
        return None
    except Exception:
        return None


def extract_base_url(url: str) -> Optional[str]:
    """
    Extract the base URL (scheme + domain) from a URL.

    Args:
        url: The full URL string.

    Returns:
        Optional[str]: The base URL, or None if invalid.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
        return None
    except Exception:
        return None


def is_valid_http_url(url: str) -> bool:
    """
    Check if a string is a valid HTTP or HTTPS URL.

    Args:
        url: The URL string to check.

    Returns:
        bool: True if valid HTTP/HTTPS URL, False otherwise.
    """
    url_pattern = re.compile(
        r"^https?://"
        r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
        r"(:\d+)?"
        r"(/[\w\-./?%&=]*)?"
        r"$"
    )
    return bool(url_pattern.match(url))


def sanitize_url(url: str) -> Optional[str]:
    """
    Sanitize a URL by ensuring it has a scheme.

    Args:
        url: The URL to sanitize.

    Returns:
        Optional[str]: The sanitized URL, or None if invalid.
    """
    if not url:
        return None

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if is_valid_http_url(url):
        return url

    return None


def is_ats_url(url: str) -> bool:
    """
    Check whether a URL belongs to a trusted ATS or job board provider.

    Args:
        url: The full URL string.

    Returns:
        bool: True if the URL is hosted on a trusted ATS provider.
    """
    if not url:
        return False
    domain = extract_domain(url)
    return is_trusted_ats_domain(domain)


def extract_ats_provider(url: str) -> Optional[str]:
    """
    Extract the trusted ATS provider domain from a URL.

    Args:
        url: The full URL string.

    Returns:
        Optional[str]: The matched ATS provider domain, or None.
    """
    if not url:
        return None
    domain = extract_domain(url)
    return get_ats_provider(domain)
