"""
Constants for reputation investigation nodes.

Shared between online_reputation_investigation_node and
reddit_investigation_node to eliminate duplication.
"""

from typing import List

# Keywords for reputation analysis
SCAM_KEYWORDS: List[str] = [
    "scam", "fraud", "fake", "phishing", "avoid", "warning",
    "illegitimate", "cheating", "dishonest", "untrustworthy",
]

POSITIVE_KEYWORDS: List[str] = [
    "legitimate", "trusted", "recommended", "great", "good",
    "professional", "reliable", "reputable", "established",
]

REPUTATION_ANALYSIS_PROMPT: str = """
You are a fraud detection expert analyzing online reputation data for a company.

Company Name: {company_name}
Company Domain: {company_domain}

Web Search Results:
{search_context}

ENTITY RESOLUTION:
First, determine whether the subject is a REAL, established company or a
NON-EXISTENT fabrication. A company with a verifiable corporate identity,
established workforce, and professional presence is legitimate even if
scammers sometimes abuse its name. Do not treat negative reports about
impersonation as evidence that the company itself is fraudulent.

Analyze the search results for CORPORATE IDENTITY SIGNALS alongside risk:
- Headcount, headquarters, and office presence
- LinkedIn and professional network presence
- Official careers / ATS application links
- Established domain age and corporate WHOIS

Then determine:
1. Is this company legitimate and real?
2. Are hiring scams or recruitment fraud reported?
3. Are fake interviews or phishing attempts reported?
4. Is there evidence of genuine hiring and trusted company presence?
5. What is the overall online reputation?

Respond with a JSON object:
{{
    "risk_score": <float between 0 and 1>,
    "overall_sentiment": "Mostly Positive" | "Mixed" | "Mostly Negative" | "Neutral",
    "legitimate_presence": true | false,
    "scam_reports_found": true | false,
    "confidence": <float between 0 and 1>,
    "summary": "<one or two sentence summary>",
    "reasoning": "<detailed analysis reasoning>",
    "key_findings": ["<list of key findings>"],
    "positive_sources": ["<list of positive source descriptions>"],
    "negative_sources": ["<list of negative source descriptions>"]
}}

Be conservative. Only flag as high risk if there is strong evidence the
company is non-existent or fraudulent. Base your analysis ONLY on the
provided search results.
"""
