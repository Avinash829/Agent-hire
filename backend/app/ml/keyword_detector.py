"""
Suspicious Keyword Detection Module.

Identifies and categorizes suspicious keywords commonly found
in fraudulent job postings.
"""

import re
from typing import List, Dict
from app.constants.ml_constants import SUSPICIOUS_KEYWORDS
from app.logging.logger import get_logger

logger = get_logger(__name__)


class KeywordDetector:
    """Detect suspicious keywords in job descriptions."""

    def __init__(self):
        self.suspicious_keywords = SUSPICIOUS_KEYWORDS
        self._compiled_patterns = self._compile_patterns()
        # Map from escaped pattern string back to original keyword
        self._pattern_to_keyword = self._build_pattern_mapping()

    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """
        Compile regex patterns for each keyword category.

        Returns:
            Dict[str, List[Pattern]]: Category -> compiled regex patterns.
        """
        patterns = {}
        for category, keywords in self.suspicious_keywords.items():
            patterns[category] = [
                re.compile(re.escape(keyword), re.IGNORECASE)
                for keyword in keywords
            ]
        return patterns

    def _build_pattern_mapping(self) -> Dict[str, str]:
        """
        Build a mapping from escaped regex pattern string to original keyword.

        Returns:
            Dict[str, str]: escaped_pattern -> original_keyword.
        """
        mapping = {}
        for category, keywords in self.suspicious_keywords.items():
            for keyword in keywords:
                escaped = re.escape(keyword)
                mapping[escaped] = keyword
        return mapping

    def detect_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        Detect suspicious keywords in the given text.

        Args:
            text: Preprocessed job description text.

        Returns:
            Dict[str, List[str]]: Categories of detected keywords.
        """
        detected = {}

        for category, patterns in self._compiled_patterns.items():
            found_keywords = []
            for pattern in patterns:
                if pattern.search(text):
                    # Return original human-readable keyword, not escaped regex
                    original = self._pattern_to_keyword.get(pattern.pattern, pattern.pattern)
                    found_keywords.append(original)

            if found_keywords:
                detected[category] = found_keywords

        return detected

    def count_suspicious_keywords(self, text: str) -> int:
        """
        Count total number of suspicious keyword occurrences.

        Args:
            text: Preprocessed job description text.

        Returns:
            int: Total count of suspicious keyword occurrences.
        """
        total_count = 0
        text_lower = text.lower()

        for category, keywords in self.suspicious_keywords.items():
            for keyword in keywords:
                count = text_lower.count(keyword)
                total_count += count

        return total_count

    def get_risk_contribution(self, text: str) -> float:
        """
        Calculate risk contribution from suspicious keywords (0-1).

        Args:
            text: Preprocessed job description text.

        Returns:
            float: Keyword-based risk score between 0 and 1.
        """
        keyword_count = self.count_suspicious_keywords(text)

        if keyword_count == 0:
            return 0.0

        max_expected_keywords = 20
        risk = min(keyword_count / max_expected_keywords, 1.0)
        return risk

