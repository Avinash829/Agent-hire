"""
Feature Extraction Module for ML Pipeline.

Extracts TF-IDF features from preprocessed job description text
for input to the classifier.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from pathlib import Path
from app.constants.ml_constants import (
    TFIDF_MAX_FEATURES,
    TFIDF_NGRAM_RANGE,
    TFIDF_MAX_DOCUMENT_FREQUENCY,
    TFIDF_MIN_DOCUMENT_FREQUENCY,
)
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)


class FeatureExtractor:
    """Extract TF-IDF features from preprocessed text."""

    def __init__(self):
        self.settings = get_settings()
        self.vectorizer = self._load_or_create_vectorizer()

    def _load_or_create_vectorizer(self) -> TfidfVectorizer:
        """
        Load existing TF-IDF vectorizer or create a new one.

        Returns:
            TfidfVectorizer: Loaded or newly created vectorizer.
        """
        vectorizer_path = Path(self.settings.tfidf_vectorizer_path)

        if vectorizer_path.exists():
            try:
                vectorizer = joblib.load(str(vectorizer_path))
                logger.info("Loaded existing TF-IDF vectorizer")
                return vectorizer
            except Exception as exception:
                logger.warning(
                    f"Failed to load vectorizer: {exception}. Creating new one."
                )

        logger.info("Creating new TF-IDF vectorizer")
        return TfidfVectorizer(
            max_features=TFIDF_MAX_FEATURES,
            ngram_range=TFIDF_NGRAM_RANGE,
            max_df=TFIDF_MAX_DOCUMENT_FREQUENCY,
            min_df=TFIDF_MIN_DOCUMENT_FREQUENCY,
            stop_words="english",
        )

    def extract_features(self, preprocessed_texts: list) -> object:
        """
        Transform preprocessed texts into TF-IDF feature vectors.

        Args:
            preprocessed_texts: List of preprocessed job description texts.

        Returns:
            object: TF-IDF feature matrix.
        """
        try:
            features = self.vectorizer.transform(preprocessed_texts)
            return features
        except Exception as exception:
            logger.error(f"Feature extraction failed: {exception}")
            raise

    def save_vectorizer(self) -> None:
        """Save the TF-IDF vectorizer to disk."""
        vectorizer_path = Path(self.settings.tfidf_vectorizer_path)
        vectorizer_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            joblib.dump(self.vectorizer, str(vectorizer_path))
            logger.info(f"TF-IDF vectorizer saved to {vectorizer_path}")
        except Exception as exception:
            logger.error(f"Failed to save vectorizer: {exception}")
            raise

    def get_feature_names(self) -> list:
        """Return the list of feature names from the vectorizer."""
        try:
            return self.vectorizer.get_feature_names_out().tolist()
        except Exception:
            return []

