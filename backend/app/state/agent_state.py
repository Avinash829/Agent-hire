"""
LangGraph Agent State Definition.

Defines the typed state schema for the agent pipeline state graph.
"""

from typing import TypedDict, Optional, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    """
    State schema for the LangGraph agent pipeline.

    Each field represents data produced or consumed by graph nodes.
    """
    job_description: str
    source_link: Optional[str]
    application_link: Optional[str]

    company_name: Optional[str]
    company_domain: Optional[str]

    whois_data: Optional[Dict[str, Any]]
    website_data: Optional[Dict[str, Any]]
    online_reputation_data: Optional[Dict[str, Any]]

    investigation_evidence: Dict[str, Any]
    gemini_reasoning: Optional[str]
    agent_risk_score: Optional[float]
    agent_verdict: Optional[str]

    # Annotated reducer safely handles parallel appends
    errors: Annotated[List[str], operator.add]