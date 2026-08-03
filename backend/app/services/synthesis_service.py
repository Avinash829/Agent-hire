"""
Synthesis Service Module.

Combines results from ML Pipeline (Pipeline A) and Agent Pipeline (Pipeline B)
into a unified, explainable fraud risk report.
"""

from typing import Dict, Any
from app.prompts.synthesis_prompts import get_verdict
from app.services.synthesis_helpers import (
    generate_reasons,
    generate_recommendations,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)

ML_WEIGHT: float = 0.4
AGENT_WEIGHT: float = 0.6


class SynthesisService:
    """Combine ML and Agent pipeline results into final assessment."""

    def synthesize(
        self,
        ml_result: Dict[str, Any],
        agent_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Synthesize ML and Agent results into a final fraud risk report.

        Args:
            ml_result: Output from the ML pipeline.
            agent_result: Output from the Agent pipeline.

        Returns:
            Dict containing:
                - overall_score: Weighted combination (0-1)
                - overall_confidence: Combined confidence score
                - verdict: Final classification
                - reasons: List of supporting reasons
                - recommendations: List of recommended actions
                - ml_score: Normalized ML score
                - agent_score: Normalized agent score
        """
        logger.info("[Synthesis] Started")

        ml_score = ml_result.get("risk_score", 0.5)
        ml_confidence = ml_result.get("confidence", 0.5)
        agent_score = agent_result.get("agent_risk_score", 0.5)

        overall_score = round(
            min(max(ML_WEIGHT * ml_score + AGENT_WEIGHT * agent_score, 0.0), 1.0),
            4,
        )
        overall_confidence = round(
            (ML_WEIGHT * ml_confidence + AGENT_WEIGHT * 0.7), 4
        )
        verdict = get_verdict(overall_score)

        reasons = generate_reasons(
            ml_result, agent_result, overall_score, verdict
        )
        recommendations = generate_recommendations(
            verdict, ml_result, agent_result
        )

        synthesis_result = {
            "overall_score": overall_score,
            "overall_confidence": overall_confidence,
            "verdict": verdict,
            "reasons": reasons,
            "recommendations": recommendations,
            "ml_score": ml_score,
            "agent_score": agent_score,
        }

        logger.info(
            "[Synthesis] Completed: score=%s, verdict=%s, confidence=%s",
            overall_score,
            verdict,
            overall_confidence,
        )
        return synthesis_result
