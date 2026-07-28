"""
LangGraph Input Node.

Validates and normalizes the input job posting data
before passing it to downstream investigation nodes.
"""

from app.state.agent_state import AgentState
from app.utils.url_utils import sanitize_url
from app.logging.logger import get_logger

logger = get_logger(__name__)


def process_input(state: AgentState) -> AgentState:
    """
    Validate and normalize the input data for the agent pipeline.

    Args:
        state: Current agent state with raw input data.

    Returns:
        AgentState: Updated state with cleaned input data.
    """
    logger.info("Processing agent pipeline input")

    cleaned_state = dict(state)
    cleaned_state["errors"] = []
    cleaned_state["investigation_evidence"] = {}

    if state.get("source_link"):
        sanitized = sanitize_url(state["source_link"])
        if sanitized:
            cleaned_state["source_link"] = sanitized
        else:
            cleaned_state["errors"].append("Invalid source link URL provided")

    if state.get("application_link"):
        sanitized = sanitize_url(state["application_link"])
        if sanitized:
            cleaned_state["application_link"] = sanitized
        else:
            cleaned_state["errors"].append("Invalid application link URL provided")

    logger.info("Input processing completed")
    return cleaned_state

