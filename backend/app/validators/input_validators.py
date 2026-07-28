"""
Input Validation Utilities.

Provides reusable validation functions for user inputs
such as URLs and text content.
"""

from urllib.parse import urlparse
import re
from app.exceptions.custom_exceptions import ValidationError


def validate_url(url: str, field_name: str = "URL") -> str:
    """
    Validate and sanitize a URL string.

    Args:
        url: The URL to validate.
        field_name: Name of the field for error messages.

    Returns:
        str: The validated URL.

    Raises:
        ValidationError: If the URL is malformed or uses an unsupported scheme.
    """
    if not url or not url.strip():
        return url

    url = url.strip()

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValidationError(
            message=f"{field_name} is not a valid URL. A valid URL must include "
            f"a scheme (http/https) and a domain name."
        )

    if parsed.scheme not in ("http", "https"):
        raise ValidationError(
            message=f"{field_name} must use http or https scheme."
        )

    dangerous_patterns = [
        r"javascript:",
        r"data:",
        r"vbscript:",
        r"file://",
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            raise ValidationError(
                message=f"{field_name} contains prohibited patterns."
            )

    return url


def validate_job_description(description: str) -> str:
    """
    Validate and sanitize a job description text.

    Args:
        description: The job description text to validate.

    Returns:
        str: The validated and sanitized description.

    Raises:
        ValidationError: If the description is too short or contains prohibited content.
    """
    if not description or not description.strip():
        raise ValidationError(
            message="Job description is required and cannot be empty."
        )

    description = description.strip()

    if len(description) < 20:
        raise ValidationError(
            message="Job description must be at least 20 characters long."
        )

    if len(description) > 10000:
        raise ValidationError(
            message="Job description must not exceed 10,000 characters."
        )

    return description

