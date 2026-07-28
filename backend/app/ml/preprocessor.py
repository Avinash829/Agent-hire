"""
Text Preprocessing Module for ML Pipeline.

Handles cleaning and normalization of job description text
before feature extraction and classification.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from app.logging.logger import get_logger

logger = get_logger(__name__)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


class TextPreprocessor:
    """Preprocess job description text for ML analysis."""

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize job description text.

        Steps:
        1. Convert to lowercase
        2. Remove HTML tags
        3. Remove URLs
        4. Remove special characters and digits
        5. Remove extra whitespace

        Args:
            text: Raw job description text.

        Returns:
            str: Cleaned and normalized text.
        """
        text = text.lower()
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from text.

        Args:
            text: Input text string.

        Returns:
            str: Text with stopwords removed.
        """
        words = text.split()
        filtered_words = [
            word for word in words if word not in self.stop_words
        ]
        return " ".join(filtered_words)

    def stem_text(self, text: str) -> str:
        """
        Apply stemming to reduce words to their root form.

        Args:
            text: Input text string.

        Returns:
            str: Text with stemmed words.
        """
        words = text.split()
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return " ".join(stemmed_words)

    def preprocess(self, text: str) -> str:
        """
        Complete preprocessing pipeline for a job description.

        Args:
            text: Raw job description text.

        Returns:
            str: Fully preprocessed text ready for feature extraction.
        """
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        text = self.stem_text(text)
        return text

