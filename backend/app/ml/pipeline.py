"""
ML Pipeline Orchestrator.

Coordinates the complete traditional ML pipeline: preprocessing,
feature extraction, classification, keyword detection, and risk scoring.

Gracefully handles missing/unfitted ML models by falling back to
keyword-only analysis when trained models are unavailable.
"""

from typing import Dict, Any
from sklearn.exceptions import NotFittedError
from app.ml.preprocessor import TextPreprocessor
from app.ml.feature_extractor import FeatureExtractor
from app.ml.classifier import JobClassifier
from app.ml.keyword_detector import KeywordDetector
from app.ml.risk_scorer import RiskScorer
from app.logging.logger import get_logger

logger = get_logger(__name__)


class MLPipeline:
    """
    Complete traditional machine learning pipeline for job fraud detection.

    This pipeline operates independently from the LangGraph agent pipeline.

    If the classifier or vectorizer models are not yet trained/fitted,
    the pipeline falls back to keyword-only analysis so the system
    remains functional while waiting for model training data.
    """

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.feature_extractor = FeatureExtractor()
        self.classifier = JobClassifier()
        self.keyword_detector = KeywordDetector()
        self.risk_scorer = RiskScorer()

    def analyze(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze a job description through the complete ML pipeline.

        Falls back to keyword-only analysis if ML models are not trained.

        Args:
            job_description: Raw job description text.

        Returns:
            Dict containing:
                - fraud_probability: Probability of being fraudulent (0-1)
                - risk_score: Normalized risk score (0-1)
                - suspicious_keywords: Detected suspicious keywords
                - confidence: Confidence in the prediction
                - risk_level: Human-readable risk level
                - risk_factors: List of risk factor descriptions
                - model_status: "active" or "fallback"
        """
        logger.info("[ML Pipeline] Starting analysis")

        logger.info("[ML Pipeline] Preprocessing text")
        preprocessed_text = self.preprocessor.preprocess(job_description)

        # Attempt full ML pipeline; fall back to keyword-only if models untrained
        try:
            logger.info("[ML Pipeline] Extracting features")
            features = self.feature_extractor.extract_features([preprocessed_text])

            logger.info("[ML Pipeline] Running classifier")
            probabilities = self.classifier.predict_proba(features)

            fraud_index = 1 if self.classifier.model.classes_[1] == 1 else 0
            fraud_probability = float(probabilities[0][fraud_index])
            logger.info("[ML Pipeline] Classification probability: %s", fraud_probability)
            model_status = "active"
        except (NotFittedError, ValueError, AttributeError) as model_error:
            logger.warning(
                "[ML Pipeline] Model not trained yet (%s). Falling back to keyword-only analysis.",
                model_error,
            )
            fraud_probability = 0.5
            model_status = "fallback"

        # Keyword detection always works (no training required)
        logger.info("[ML Pipeline] Detecting keywords")
        suspicious_keywords = self.keyword_detector.detect_keywords(
            job_description.lower()
        )
        keyword_risk = self.keyword_detector.get_risk_contribution(
            job_description.lower()
        )
        logger.info(
            "[ML Pipeline] Keyword detection: %d categories",
            len(suspicious_keywords),
        )

        logger.info("[ML Pipeline] Calculating risk score")
        risk_score = self.risk_scorer.calculate_risk_score(
            fraud_probability, keyword_risk
        )
        if model_status == "fallback":
            confidence = 0.5  # Moderate confidence when model is unavailable
        else:
            confidence = self.risk_scorer.calculate_confidence(fraud_probability)
        risk_level = self.risk_scorer.get_risk_level(risk_score)
        risk_factors = self.risk_scorer.get_risk_factors(
            suspicious_keywords, risk_score
        )

        all_keywords = []
        for category_keywords in suspicious_keywords.values():
            all_keywords.extend(category_keywords)

        result = {
            "fraud_probability": round(fraud_probability, 4),
            "risk_score": risk_score,
            "suspicious_keywords": all_keywords,
            "confidence": confidence,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "model_status": model_status,
        }

        logger.info(
            "[ML Pipeline] Completed: model=%s, risk_score=%s, level=%s",
            model_status,
            risk_score,
            risk_level,
        )
        return result

