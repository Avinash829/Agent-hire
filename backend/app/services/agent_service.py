"""
Agent Service Module.

Wraps the LangGraph agent pipeline for use by the verification service.
Provides a clean interface for executing agent investigations.
"""

from typing import Dict, Any
from app.agents.graph import run_agent_pipeline
from app.logging.logger import get_logger

logger = get_logger(__name__)


class AgentService:
    """Service for executing the LangGraph agent pipeline."""

    async def investigate(
        self,
        job_description: str,
        source_link: str = None,
        application_link: str = None,
    ) -> Dict[str, Any]:
        """
        Execute the full agent pipeline on a job posting.

        Args:
            job_description: The job posting text to analyze.
            source_link: URL where the job was found.
            application_link: URL for job applications.

        Returns:
            Dict containing:
                - company_name: Extracted company name
                - company_domain: Extracted company domain
                - investigation_evidence: Structured evidence
                - gemini_reasoning: LLM reasoning text
                - agent_risk_score: Risk score (0-1)
                - agent_verdict: Verdict (fraudulent/suspicious/legitimate)
                - errors: List of any errors encountered
        """
        logger.info("[Agent Service] Started")

        input_data = {
            "job_description": job_description,
            "source_link": source_link,
            "application_link": application_link,
        }

        try:
            result = await run_agent_pipeline(input_data)
            logger.info(
                "[Agent Service] Completed: verdict=%s",
                result.get("agent_verdict"),
            )
            return result
        except Exception as exception:
            logger.exception("[Agent Service] Failed: %s", str(exception))
            return {
                "company_name": None,
                "company_domain": None,
                "investigation_evidence": {"error": str(exception)},
                "gemini_reasoning": "Investigation failed",
                "agent_risk_score": 0.5,
                "agent_verdict": "unavailable",
                "errors": [str(exception)],
            }

