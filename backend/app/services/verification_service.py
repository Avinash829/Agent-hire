"""
Verification Service Module.

Orchestrates the complete verification flow: running ML and Agent
pipelines in parallel and synthesizing results.
"""

import asyncio
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
from app.ml.pipeline import MLPipeline
from app.services.agent_service import AgentService
from app.services.synthesis_service import SynthesisService
from app.repositories.verification_repository import VerificationRepository
from app.models.verification import VerificationDocument
from app.logging.logger import get_logger

logger = get_logger(__name__)


class VerificationService:
    """
    Orchestrates the hybrid verification process.

    Runs ML Pipeline (A) and Agent Pipeline (B) independently,
    then combines results via synthesis service.
    """

    def __init__(
        self,
        ml_pipeline: MLPipeline,
        agent_service: AgentService,
        synthesis_service: SynthesisService,
        repository: VerificationRepository,
    ):
        self.ml_pipeline = ml_pipeline
        self.agent_service = agent_service
        self.synthesis_service = synthesis_service
        self.repository = repository

    async def verify_job_posting(
        self,
        job_description: str,
        firebase_uid: str,
        source_link: Optional[str] = None,
        application_link: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute complete verification of a job posting.

        Runs both pipelines independently and synthesizes results.

        Args:
            job_description: The job posting text.
            firebase_uid: Authenticated user's Firebase UID.
            source_link: Source URL of the job posting.
            application_link: Application URL.

        Returns:
            Dict: Complete verification result with insights from both pipelines.
        """
        verification_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        logger.info(
            "[Verification] Started: ID=%s for user=%s",
            verification_id,
            firebase_uid,
        )

        # Run ML pipeline in thread pool to avoid blocking the event loop
        logger.info("[ML Pipeline] Started")
        loop = asyncio.get_event_loop()
        ml_result = await loop.run_in_executor(
            None, self.ml_pipeline.analyze, job_description
        )
        logger.info("[ML Pipeline] Completed")

        logger.info("[Agent Service] Started")
        agent_result = await self.agent_service.investigate(
            job_description=job_description,
            source_link=source_link,
            application_link=application_link,
        )
        logger.info("[Agent Service] Completed")

        logger.info("[Synthesis] Started")
        synthesis = self.synthesis_service.synthesize(ml_result, agent_result)
        logger.info("[Synthesis] Completed")

        combined_evidence = {
            "ml_analysis": ml_result,
            "agent_investigation": agent_result.get("investigation_evidence", {}),
        }

        # agent_risk_score already defaults to 0.5 inside graph.run_agent_pipeline()
        agent_score = agent_result.get("agent_risk_score", 0.5)

        verification_document = VerificationDocument(
            _id=verification_id,
            firebase_uid=firebase_uid,
            job_description=job_description,
            source_link=source_link,
            application_link=application_link,
            ml_score=ml_result.get("risk_score", 0.5),
            ml_confidence=ml_result.get("confidence", 0.5),
            agent_score=agent_score,
            final_score=synthesis["overall_score"],
            verdict=synthesis["verdict"],
            reasons=synthesis["reasons"],
            recommendations=synthesis["recommendations"],
            evidence=combined_evidence,
            ml_result=ml_result,
            agent_result=agent_result,
            timestamp=timestamp,
        )

        await self.repository.create_verification(verification_document)
        logger.info("[MongoDB] Verification Saved: ID=%s", verification_id)

        logger.info(
            "[Verification] Completed: ID=%s, verdict=%s",
            verification_id,
            synthesis["verdict"],
        )

        return {
            "success": True,
            "verification_id": verification_id,
            "ml_result": {
                "fraud_probability": ml_result.get("fraud_probability"),
                "risk_score": ml_result.get("risk_score"),
                "suspicious_keywords": ml_result.get("suspicious_keywords", []),
                "confidence": ml_result.get("confidence"),
            },
            "agent_result": {
                "company_name": agent_result.get("company_name"),
                "company_domain": agent_result.get("company_domain"),
                "agent_verdict": agent_result.get("agent_verdict"),
                "gemini_reasoning": agent_result.get("gemini_reasoning"),
                "agent_risk_score": agent_result.get("agent_risk_score"), # <-- ADD THIS LINE
            },
            "synthesis": synthesis,
            "evidence": combined_evidence,
            "timestamp": timestamp.isoformat(),
        }
