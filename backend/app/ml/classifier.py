"""
Classification Module for ML Pipeline.

Uses a Random Forest classifier to predict whether a job posting
is fraudulent based on TF-IDF features.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import numpy as np
from pathlib import Path
from app.constants.ml_constants import (
    RANDOM_FOREST_N_ESTIMATORS,
    RANDOM_FOREST_MAX_DEPTH,
    RANDOM_FOREST_MIN_SAMPLES_SPLIT,
    RANDOM_FOREST_MIN_SAMPLES_LEAF,
    RANDOM_FOREST_RANDOM_STATE,
)
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)


class JobClassifier:
    """Classify job postings as fraudulent or legitimate."""

    def __init__(self):
        self.settings = get_settings()
        self.model = self._load_or_create_model()

    def _load_or_create_model(self) -> RandomForestClassifier:
        """
        Load existing model or create a new Random Forest classifier.

        Returns:
            RandomForestClassifier: Loaded or newly created classifier.
        """
        model_path = Path(self.settings.classifier_model_path)

        if model_path.exists():
            try:
                model = joblib.load(str(model_path))
                logger.info("Loaded existing classifier model")
                return model
            except Exception as exception:
                logger.warning(
                    f"Failed to load model: {exception}. Creating new one."
                )

        logger.warning(
            "[ML Pipeline] No saved model found at %s. Creating untrained model. "
            "The ML pipeline will use keyword-only fallback until a model is trained.",
            self.settings.classifier_model_path,
        )
        return RandomForestClassifier(
            n_estimators=RANDOM_FOREST_N_ESTIMATORS,
            max_depth=RANDOM_FOREST_MAX_DEPTH,
            min_samples_split=RANDOM_FOREST_MIN_SAMPLES_SPLIT,
            min_samples_leaf=RANDOM_FOREST_MIN_SAMPLES_LEAF,
            random_state=RANDOM_FOREST_RANDOM_STATE,
            n_jobs=-1,
        )

    def predict(self, features: object) -> np.ndarray:
        """
        Predict fraud labels for job descriptions.

        Args:
            features: TF-IDF feature matrix.

        Returns:
            np.ndarray: Array of predictions (0: legitimate, 1: fraudulent).
        """
        try:
            predictions = self.model.predict(features)
            return predictions
        except Exception as exception:
            logger.error(f"Classification prediction failed: {exception}")
            raise

    def predict_proba(self, features: object) -> np.ndarray:
        """
        Predict fraud probabilities for job descriptions.

        Args:
            features: TF-IDF feature matrix.

        Returns:
            np.ndarray: Array of probability estimates.
        """
        try:
            probabilities = self.model.predict_proba(features)
            return probabilities
        except Exception as exception:
            logger.error(f"Probability prediction failed: {exception}")
            raise

    def train(
        self, features: object, labels: np.ndarray
    ) -> dict:
        """
        Train the classifier on labeled data.

        Args:
            features: TF-IDF feature matrix.
            labels: Ground truth labels (0: legitimate, 1: fraudulent).

        Returns:
            dict: Training metrics (accuracy, precision, recall, f1).
        """
        try:
            (
                features_train,
                features_test,
                labels_train,
                labels_test,
            ) = train_test_split(
                features, labels, test_size=0.2, random_state=42
            )

            self.model.fit(features_train, labels_train)

            predictions = self.model.predict(features_test)

            metrics = {
                "accuracy": float(accuracy_score(labels_test, predictions)),
                "precision": float(
                    precision_score(labels_test, predictions, average="binary")
                ),
                "recall": float(
                    recall_score(labels_test, predictions, average="binary")
                ),
                "f1_score": float(
                    f1_score(labels_test, predictions, average="binary")
                ),
            }

            logger.info(f"Model training completed. Metrics: {metrics}")
            return metrics

        except Exception as exception:
            logger.error(f"Model training failed: {exception}")
            raise

    def save_model(self) -> None:
        """Save the trained model to disk."""
        model_path = Path(self.settings.classifier_model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            joblib.dump(self.model, str(model_path))
            logger.info(f"Classifier model saved to {model_path}")
        except Exception as exception:
            logger.error(f"Failed to save model: {exception}")
            raise

