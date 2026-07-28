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

Analyze the evidence and respond with a JSON object:
{{
    "fraud_verdict": "fraudulent" | "suspicious" | "legitimate",
    "confidence": <float between 0 and 1>,
    "risk_score": <float between 0 and 1>,
    "reasoning": "<detailed explanation of your verdict>",
    "red_flags": ["<list of red flags identified>"],
    "positive_indicators": ["<list of positive indicators>"]
}}

Be conservative. Only label as "fraudulent" if there is strong evidence.

Consider:
1. Is the company legitimate and well-known?
2. Does the domain registration look suspicious?
3. Does the career page look professional?
4. Are there scam reports, phishing reports, or reputation issues found online?
5. Does the overall evidence suggest fraud?
"""

