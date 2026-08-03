"""
Synthesis Helper Functions.

Generates human-readable reasons and recommendations for the
synthesis service, keeping the main module concise.
"""

from typing import Dict, Any


def generate_reasons(
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
    if website.get("ats_provider_detected"):
        reasons.append(
            f"[Website Check] Official career application via "
            f"trusted ATS: {website.get('ats_provider', 'provider')}"
        )
    elif not website.get("has_career_page"):
        reasons.append(
            "[Website Check] No career page found on company website"
        )

    online_reputation = evidence.get("online_reputation", {})
    if online_reputation.get("scam_mentions", 0) > 0:
        reasons.append(
            "[Online Reputation Check] Scam reports found in "
            "online reputation sources"
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


def generate_recommendations(
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
