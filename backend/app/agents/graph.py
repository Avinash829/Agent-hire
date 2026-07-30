"""
LangGraph Agent Pipeline Graph Definition.

Defines the StateGraph with all investigation nodes and their
execution flow for parallel job fraud investigation.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph
from app.state.agent_state import AgentState
from app.agents.input_node import process_input
from app.agents.company_extraction_node import extract_company
from app.agents.whois_investigation_node import investigate_whois
from app.agents.website_investigation_node import investigate_website
from app.agents.online_reputation_investigation_node import investigate_online_reputation
from app.agents.evidence_aggregation_node import aggregate_evidence
from app.agents.gemini_reasoning_node import gemini_reasoning
from app.logging.logger import get_logger

logger = get_logger(__name__)


def build_agent_graph() -> StateGraph:
    """
    Build and compile the LangGraph agent pipeline.

    Flow:
    Input → Company Extraction → Parallel (WHOIS, Website, Online Reputation)
    → Evidence Aggregation → Gemini Reasoning → Result

    Returns:
        StateGraph: Compiled LangGraph state graph.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("input", process_input)
    workflow.add_node("extract_company", extract_company)
    workflow.add_node("investigate_whois", investigate_whois)
    workflow.add_node("investigate_website", investigate_website)
    workflow.add_node("investigate_online_reputation", investigate_online_reputation)
    workflow.add_node("aggregate_evidence", aggregate_evidence)
    workflow.add_node("gemini_reason", gemini_reasoning)

    workflow.set_entry_point("input")

    workflow.add_edge("input", "extract_company")

    workflow.add_edge("extract_company", "investigate_whois")
    workflow.add_edge("extract_company", "investigate_website")
    workflow.add_edge("extract_company", "investigate_online_reputation")

    workflow.add_edge("investigate_whois", "aggregate_evidence")
    workflow.add_edge("investigate_website", "aggregate_evidence")
    workflow.add_edge("investigate_online_reputation", "aggregate_evidence")

    workflow.add_edge("aggregate_evidence", "gemini_reason")

    graph = workflow.compile()
    logger.info("Agent pipeline graph compiled successfully")
    return graph


_agent_graph = None


def get_agent_graph() -> StateGraph:
    """
    Return cached agent graph instance (singleton pattern).

    Returns:
        StateGraph: Compiled LangGraph state graph.
    """
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = build_agent_graph()
    return _agent_graph


async def run_agent_pipeline(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the agent pipeline with given input data.

    Args:
        input_data: Dictionary with job_description, source_link, application_link.

    Returns:
        Dict: Agent pipeline results including investigation evidence and verdict.
    """
    logger.info("[Agent Pipeline] Started")

    graph = get_agent_graph()

    initial_state: AgentState = {
        "job_description": input_data.get("job_description", ""),
        "source_link": input_data.get("source_link"),
        "application_link": input_data.get("application_link"),
        "company_name": None,
        "company_domain": None,
        "whois_data": None,
        "website_data": None,
        "online_reputation_data": None,
        "investigation_evidence": {},
        "gemini_reasoning": None,
        "agent_risk_score": None,
        "agent_verdict": None,
        "errors": [],
    }

    try:
        final_state = await graph.ainvoke(initial_state)

        result = {
            "company_name": final_state.get("company_name"),
            "company_domain": final_state.get("company_domain"),
            "investigation_evidence": final_state.get("investigation_evidence", {}),
            "gemini_reasoning": final_state.get("gemini_reasoning"),
            "agent_risk_score": final_state.get("agent_risk_score", 0.5),
            "agent_verdict": final_state.get("agent_verdict", "suspicious"),
            "errors": final_state.get("errors", []),
        }

        logger.info(
            "[Agent Pipeline] Completed: "
            f"verdict={result['agent_verdict']}, "
            f"score={result['agent_risk_score']}"
        )
        return result

    except Exception as exception:
        logger.exception("[Agent Pipeline] Failed: %s", str(exception))
        raise

