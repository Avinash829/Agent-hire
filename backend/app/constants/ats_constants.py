"""
ATS & Job Board Trusted Domain Constants.

Defines the comprehensive list of trusted Applicant Tracking System (ATS)
providers and job boards. When an application or job link matches any of
these providers, the system treats it as a legitimate career application
channel, bypassing the need for the company's root domain to host the job.
"""

from typing import List, Optional

# Global enterprise ATS providers
GLOBAL_ATS_DOMAINS: List[str] = [
    "greenhouse.io",
    "lever.co",
    "myworkdayjobs.com",
    "bamboohr.com",
    "smartrecruiters.com",
    "icims.com",
    "taleo.net",
    "workable.com",
    "linkedin.com",
    "indeed.com",
    "wellfound.com",
]

# Indian / APAC regional ATS providers and job boards
REGIONAL_ATS_DOMAINS: List[str] = [
    "keka.com",
    "darwinbox.com",
    "darwinbox.in",
    "zoho.com",
    "zohorecruit.com",
    "instahyre.com",
    "hirist.com",
    "cutshort.io",
    "naukri.com",
    "foundit.in",
    "internshala.com",
]

# Combined list of all trusted ATS/job board domains
TRUSTED_ATS_DOMAINS: List[str] = GLOBAL_ATS_DOMAINS + REGIONAL_ATS_DOMAINS


def is_trusted_ats_domain(domain: Optional[str]) -> bool:
    """
    Check whether a domain is a trusted ATS or job board provider.

    Performs an exact match against the trusted domain list. Subdomains
    of a trusted provider (e.g. jobs.acme.greenhouse.io) are resolved to
    the base provider domain via the suffix check.

    Args:
        domain: The domain string to check (may include subdomains).

    Returns:
        bool: True if the domain belongs to a trusted ATS provider.
    """
    if not domain:
        return False

    domain = domain.strip().lower()

    for trusted in TRUSTED_ATS_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True

    return False


def get_ats_provider(domain: Optional[str]) -> Optional[str]:
    """
    Return the matched trusted ATS provider domain for a given domain.

    Args:
        domain: The domain string to resolve.

    Returns:
        Optional[str]: The trusted provider domain, or None if unmatched.
    """
    if not domain:
        return None

    domain = domain.strip().lower()

    for trusted in TRUSTED_ATS_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return trusted

    return None


__all__ = [
    "GLOBAL_ATS_DOMAINS",
    "REGIONAL_ATS_DOMAINS",
    "TRUSTED_ATS_DOMAINS",
    "is_trusted_ats_domain",
    "get_ats_provider",
]
