"""
Agent Pipeline Constants.

Defines configuration constants for the LangGraph agent pipeline.
"""

# WHOIS Investigation
MINIMUM_DOMAIN_AGE_DAYS: int = 180
SUSPICIOUS_REGISTRARS: list = [
    "namecheap", "godaddy", "enom", "porkbun",
    "namebright", "namesilo", "dynadot",
]

# Website Investigation
REQUEST_TIMEOUT_SECONDS: int = 15
MAX_REDIRECT_FOLLOWS: int = 5
CAREER_PAGE_KEYWORDS: list = [
    "career", "jobs", "careers", "join us", "work with us",
    "employment", "opportunities", "open positions", "vacancies",
    "hiring", "recruitment", "talent", "we are hiring",
]

# Tavily Web Reputation Investigation
TAVILY_MAX_RESULTS: int = 5
TAVILY_SEARCH_DEPTH: str = "basic"

URL_FETCH_TIMEOUT: int = 10

# Agent Weights (for synthesis)
AGENT_INVESTIGATION_WEIGHT: float = 0.5
GEMINI_REASONING_WEIGHT: float = 0.5

# Parallel Execution
MAX_PARALLEL_INVESTIGATIONS: int = 3

