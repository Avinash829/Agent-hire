"""
Synthesis Service Module.

Combines results from ML Pipeline (Pipeline A) and Agent Pipeline (Pipeline B)
into a unified, explainable fraud risk report.
"""

from typing import Dict, Any
from app.prompts.synthesis_prompts import get_verdict
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
        logger.info("Synthesizing ML and Agent pipeline results")

        ml_score = ml_result.get("risk_score", 0.5)
        ml_confidence = ml_result.get("confidence", 0.5)

        agent_score = agent_result.get("agent_risk_score", 0.5)

        if agent_score is None:
            agent_score = 0.5

        overall_score = (
            ML_WEIGHT * ml_score + AGENT_WEIGHT * agent_score
        )
        overall_score = round(min(max(overall_score, 0.0), 1.0), 4)

        overall_confidence = round(
            (ML_WEIGHT * ml_confidence + AGENT_WEIGHT * 0.7), 4
        )

        verdict = get_verdict(overall_score)

        reasons = self._generate_reasons(
            ml_result, agent_result, overall_score, verdict
        )
        recommendations = self._generate_recommendations(
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
            f"Synthesis completed: score={overall_score}, "
            f"verdict={verdict}, confidence={overall_confidence}"
        )
        return synthesis_result

    def _generate_reasons(
        self,
        ml_result: Dict[str, Any],
        agent_result: Dict[str, Any],
        overall_score: float,
        verdict: str,
    ) -> list:
        """
        Generate human-readable reasons for the verdict.

        Args:
            ml_result: ML pipeline result.
            agent_result: Agent pipeline result.
            overall_score: Combined risk score.
            verdict: Final verdict.

        Returns:
            list: Reason descriptions.
        """
        reasons = []

        ml_risk_factors = ml_result.get("risk_factors", [])
        if ml_risk_factors:
            for factor in ml_risk_factors[:3]:
                reasons.append(f"[ML Analysis] {factor}")

        agent_verdict = agent_result.get("agent_verdict", "")
        if agent_verdict:
            reasons.append(
                f"[AI Investigation] Agent analysis suggests: {agent_verdict}"
            )

        evidence = agent_result.get("investigation_evidence", {})
        whois = evidence.get("whois", {})
        if whois.get("is_suspiciously_young"):
            reasons.append(
                "[Domain Check] Company domain was registered recently, "
                "which is suspicious for legitimate employers"
            )

        website = evidence.get("website", {})
        if not website.get("has_career_page"):
            reasons.append(
                "[Website Check] No career page found on company website"
            )

        online_reputation = evidence.get("online_reputation", {})
        if online_reputation.get("scam_mentions", 0) > 0:
            reasons.append(
                "[Online Reputation Check] Scam reports found in online reputation sources"
            )

        if not reasons:
            if verdict == "legitimate":
                reasons.append(
                    "No significant fraud indicators detected across both pipelines"
                )
            else:
                reasons.append(
                    f"Combined analysis indicates {verdict} posting with "
                    f"risk score of {overall_score:.2f}"
                )

        return reasons

    def _generate_recommendations(
        self,
        verdict: str,
        ml_result: Dict[str, Any],
        agent_result: Dict[str, Any],
    ) -> list:
        """
        Generate actionable recommendations based on the verdict.

        Args:
            verdict: Final verdict.
            ml_result: ML pipeline result.
            agent_result: Agent pipeline result.

        Returns:
            list: Recommendation descriptions.
        """
        recommendations = []

        if verdict == "fraudulent":
            recommendations.extend([
                "Do not apply for this position",
                "Report the job posting to the platform where it was found",
                "Avoid sharing any personal or financial information",
                "Block the poster if contacted directly",
            ])
        elif verdict == "suspicious":
            recommendations.extend([
                "Verify the company through official channels before applying",
                "Search for additional reviews of the company",
                "Do not provide payment or sensitive information upfront",
                "Check the company's presence on professional networks like LinkedIn",
            ])
        elif verdict == "legitimate":
            recommendations.extend([
                "Proceed with application through official channels",
                "Verify the application link matches the company domain",
                "Monitor for any unusual requests during the hiring process",
            ])

        return recommendations

