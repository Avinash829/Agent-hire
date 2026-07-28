"""
Risk Scoring Module for ML Pipeline.

Combines classifier predictions and keyword analysis into
a unified risk score.
"""

from typing import Dict, Any
from app.constants.ml_constants import (
    CLASSIFIER_WEIGHT,
    KEYWORD_WEIGHT,
    LOW_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    HIGH_RISK_THRESHOLD,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)


class RiskScorer:
    """Calculate and interpret risk scores from ML analysis."""

    def calculate_risk_score(
        self,
        classifier_probability: float,
        keyword_risk: float,
    ) -> float:
        """
        Calculate weighted risk score from classifier and keyword analysis.

        Args:
            classifier_probability: Probability from classifier (fraud class).
            keyword_risk: Risk score from keyword detection (0-1).

        Returns:
            float: Weighted risk score between 0 and 1.
        """
        risk_score = (
            CLASSIFIER_WEIGHT * classifier_probability
            + KEYWORD_WEIGHT * keyword_risk
        )
        return round(min(max(risk_score, 0.0), 1.0), 4)

    def get_risk_level(self, risk_score: float) -> str:
        """
        Categorize risk score into a human-readable level.

        Args:
            risk_score: Calculated risk score (0-1).

        Returns:
            str: Risk level: 'low', 'medium', 'high', or 'critical'.
        """
        if risk_score >= HIGH_RISK_THRESHOLD:
            return "critical"
        elif risk_score >= MEDIUM_RISK_THRESHOLD:
            return "high"
        elif risk_score >= LOW_RISK_THRESHOLD:
            return "medium"
        else:
            return "low"

    def calculate_confidence(self, probability: float) -> float:
        """
        Calculate confidence score based on prediction probability.

        Confidence is highest when probability is near extremes (0 or 1).

        Args:
            probability: Prediction probability (0-1).

        Returns:
            float: Confidence score between 0 and 1.
        """
        confidence = 1.0 - (2.0 * abs(probability - 0.5))
        return round(confidence, 4)

    def get_risk_factors(
        self,
        suspicious_keywords: Dict[str, list],
        risk_score: float,
    ) -> list:
        """
        Generate human-readable risk factors based on analysis.

        Args:
            suspicious_keywords: Detected suspicious keywords by category.
            risk_score: Overall risk score.

        Returns:
            list: Risk factor descriptions.
        """
        risk_factors = []

        if risk_score >= HIGH_RISK_THRESHOLD:
            risk_factors.append(
                "Job posting exhibits multiple high-risk indicators"
            )
        elif risk_score >= MEDIUM_RISK_THRESHOLD:
            risk_factors.append(
                "Job posting shows several suspicious patterns"
            )

        for category, keywords in suspicious_keywords.items():
            category_labels = {
                "high_income": "Unrealistic income claims detected",
                "no_experience_required": "No experience requirement raises suspicion",
                "urgency_pressure": "High-pressure urgency tactics detected",
                "suspicious_requests": "Monetary requests detected in posting",
                "vague_benefits": "Vague or exaggerated benefits mentioned",
                "unprofessional": "Unprofessional hiring language detected",
            }

            label = category_labels.get(category, f"Suspicious pattern: {category}")
            risk_factors.append(label)

        return risk_factors

