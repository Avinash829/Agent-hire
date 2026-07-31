"""
LangGraph WHOIS Investigation Node.

Performs WHOIS domain lookup to assess domain registration
legitimacy and age.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
import whois
from app.state.agent_state import AgentState
from app.constants.agent_constants import MINIMUM_DOMAIN_AGE_DAYS
from app.logging.logger import get_logger

logger = get_logger(__name__)


def investigate_whois(state: AgentState) -> dict:
    """
    Perform WHOIS lookup on the company domain.
    """
    logger.info("[WHOIS] Started")

    domain = state.get("company_domain")
    logger.info("[WHOIS] Lookup started for domain: %s", domain)

    if not domain:
        logger.warning("[WHOIS] No domain available for lookup")
        logger.info("[WHOIS] Completed (no domain)")
        return {"whois_data": {"error": "No domain available"}}

    whois_data = {"domain": domain}

    try:
        logger.info("[WHOIS] Sending WHOIS lookup request for %s", domain)
        domain_info = whois.whois(domain)
        logger.info("[WHOIS] WHOIS response received for %s", domain)

        creation_date = domain_info.creation_date
        registrar = domain_info.registrar
        expiration_date = domain_info.expiration_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if creation_date:
            if isinstance(creation_date, str):
                creation_date = datetime.fromisoformat(
                    creation_date.replace("Z", "+00:00")
                )
            elif isinstance(creation_date, datetime):
                if creation_date.tzinfo is None:
                    creation_date = creation_date.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)
            age_days = (now - creation_date).days
            whois_data["age_days"] = age_days
            whois_data["creation_date"] = creation_date.isoformat()
            whois_data["is_suspiciously_young"] = age_days < MINIMUM_DOMAIN_AGE_DAYS
        else:
            whois_data["age_days"] = None
            whois_data["is_suspiciously_young"] = True

        if registrar:
            whois_data["registrar"] = registrar
        else:
            whois_data["registrar"] = "Unknown"

        if expiration_date:
            if isinstance(expiration_date, str):
                expiration_date = datetime.fromisoformat(
                    expiration_date.replace("Z", "+00:00")
                )
            whois_data["expiration_date"] = expiration_date.isoformat()

        whois_data["status"] = "completed"
        logger.info(
            "[WHOIS] Lookup completed for %s: "
            "age=%s days, registrar=%s",
            domain,
            whois_data.get("age_days"),
            whois_data.get("registrar"),
        )

        return {"whois_data": whois_data}

    except Exception as exception:
        logger.exception("[WHOIS] Failed for %s: %s", domain, str(exception))
        whois_data["status"] = "failed"
        whois_data["error"] = str(exception)
        
        return {
            "whois_data": whois_data,
            "errors": [f"WHOIS investigation failed: {str(exception)[:200]}"]
        }