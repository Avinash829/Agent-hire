"""
Synthesis Prompt Templates.

Defines prompt templates for the synthesis service
when combining ML and Agent pipeline results.
"""

COMBINATION_STRATEGY = """
Combination Strategy:

The ML Score represents text-based pattern analysis.
The Agent Score represents investigative evidence analysis.

The final score is calculated as:

final_score = (ml_weight * ml_score) + (agent_weight * agent_score)

Where:
- ml_weight = 0.4
- agent_weight = 0.6

The agent score is given higher weight because it incorporates
evidence from multiple real-world sources.
"""

VERDICT_THRESHOLDS = {
    "legitimate": {"max_score": 0.3},
    "suspicious": {"min_score": 0.3, "max_score": 0.65},
    "fraudulent": {"min_score": 0.65},
}


def get_verdict(final_score: float) -> str:
    """
    Determine the final verdict based on the combined score.

    Args:
        final_score: Combined risk score between 0 and 1.

    Returns:
        str: 'legitimate', 'suspicious', or 'fraudulent'.
    """
    for verdict, thresholds in VERDICT_THRESHOLDS.items():
        min_score = thresholds.get("min_score", 0.0)
        max_score = thresholds.get("max_score", 1.0)

        if min_score <= final_score <= max_score:
            return verdict

    return "suspicious"

