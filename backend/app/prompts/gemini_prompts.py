"""
Gemini LLM Prompt Templates.

Defines prompt templates used for Gemini reasoning over
collected investigation evidence.
"""

COMPANY_EXTRACTION_PROMPT = """
You are an expert at extracting company information from job postings.

Given the following job description, extract:

1. Company name
2. Any website URLs mentioned

Job Description:
{job_description}

Respond with a JSON object:
{{
    "company_name": "Extracted company name or null if not found",
    "mentioned_urls": ["List of URLs found in the description"]
}}
"""

REASONING_PROMPT = """
You are a fraud detection expert analyzing a job posting.
Given the following evidence from multiple investigation sources,
determine if this job posting is likely fraudulent.

Job Description Preview:
{job_description_preview}

Extracted Company Name: {company_name}

WHOIS Investigation:
{whois_data}

Website Investigation:
{website_data}

Online Reputation Investigation (Tavily Search):
{online_reputation_data}

ENTITY RESOLUTION - CRITICAL:
First, distinguish between two distinct scenarios:
1. A NON-EXISTENT / FAKE company invented by scammers with no real
   corporate identity, no genuine website, and no established workforce.
2. SCAMMERS IMPERSONATING a REAL, legitimate company. When the evidence
   shows a genuine company with a real domain, real ATS career links,
   established headcount, and corporate presence, the company itself is
   legitimate even if a scammer may be abusing its name.

Only flag the company as fraudulent when the evidence indicates a
non-existent entity. If the company is real but its name is being
impersonated, the job posting may be fraudulent but the company
is NOT the fraudster.

BALANCING LEGITIMACY SIGNALS:
Strong legitimacy signals should meaningfully reduce risk:
- Domain age greater than 2 years (730+ days)
- Official ATS provider career links (greenhouse, lever, workday, etc.)
- Corporate WHOIS with established registrar history
- Established workforce and professional online presence

Analyze the evidence and respond with a JSON object:
{{
    "fraud_verdict": "fraudulent" | "suspicious" | "legitimate",
    "confidence": <float between 0 and 1>,
    "risk_score": <float between 0 and 1>,
    "reasoning": "<detailed explanation of your verdict>",
    "red_flags": ["<list of red flags identified>"],
    "positive_indicators": ["<list of positive indicators>"]
}}

Be conservative. Only label as "fraudulent" if there is strong evidence
that the company itself is non-existent or fraudulent.

Consider:
1. Is there a real, established company behind this posting?
2. Does the domain registration look suspicious or too young?
3. Does the career page look professional (or use a trusted ATS)?
4. Are there scam reports, phishing reports, or reputation issues?
5. Does the overall evidence suggest the COMPANY is non-existent/fake?
"""
