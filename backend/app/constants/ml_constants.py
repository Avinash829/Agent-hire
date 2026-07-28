"""
ML Pipeline Constants.

Defines configuration constants for the traditional machine learning pipeline.
"""

# TF-IDF Vectorizer Configuration
TFIDF_MAX_FEATURES: int = 5000
TFIDF_NGRAM_RANGE: tuple = (1, 2)
TFIDF_MAX_DOCUMENT_FREQUENCY: float = 0.85
TFIDF_MIN_DOCUMENT_FREQUENCY: int = 2

# Random Forest Classifier Configuration
RANDOM_FOREST_N_ESTIMATORS: int = 100
RANDOM_FOREST_MAX_DEPTH: int = 20
RANDOM_FOREST_MIN_SAMPLES_SPLIT: int = 5
RANDOM_FOREST_MIN_SAMPLES_LEAF: int = 2
RANDOM_FOREST_RANDOM_STATE: int = 42

# Risk Scoring Weights
KEYWORD_WEIGHT: float = 0.3
CLASSIFIER_WEIGHT: float = 0.7

# Suspicious Keywords Categories
SUSPICIOUS_KEYWORDS: dict = {
    "high_income": [
        "work from home", "earn money", "get rich", "quick cash",
        "unlimited income", "financial freedom", "passive income",
        "make money fast", "easy money",
    ],
    "no_experience_required": [
        "no experience", "no skills", "anyone can apply",
        "no qualification", "entry level no experience",
        "no degree needed", "start immediately",
    ],
    "urgency_pressure": [
        "urgent hiring", "limited positions", "act now",
        "immediate start", "apply today", "hurry",
        "limited time offer", "don't miss out",
    ],
    "suspicious_requests": [
        "pay to apply", "processing fee", "registration fee",
        "training fee", "money upfront", "send money",
        "wire transfer", "bank details required",
    ],
    "vague_benefits": [
        "unlimited earning potential", "be your own boss",
        "work your own hours", "life changing opportunity",
        "ground floor opportunity", "amazing opportunity",
    ],
    "unprofessional": [
        "guaranteed job", "100% placement", "no interview",
        "direct hiring", "secret hiring", "confidential",
    ],
}

# Risk Thresholds
LOW_RISK_THRESHOLD: float = 0.3
MEDIUM_RISK_THRESHOLD: float = 0.6
HIGH_RISK_THRESHOLD: float = 0.8

