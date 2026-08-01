"""
LangGraph Gemini Reasoning Node.

Uses Gemini LLM to reason over collected investigation evidence
and produce a final fraud assessment.
"""

import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.state.agent_state import AgentState
from app.config.settings import get_settings
from app.prompts.gemini_prompts import REASONING_PROMPT
from app.utils.text_utils import parse_json_response
from app.logging.logger import get_logger
from app.agents.common.llm_factory import get_gemini_llm_with_fallbacks

logger = get_logger(__name__)


def gemini_reasoning(state: AgentState) -> AgentState:
    """
    Use Gemini LLM to analyze investigation evidence and produce verdict.

    Args:
        state: Current agent state with aggregated evidence.

    Returns:
        AgentState: State with Gemini reasoning results.
    """
    logger.info("[Gemini Reasoning] Started")

    updated_state = dict(state)
    evidence = state.get("investigation_evidence", {})
    job_description = state.get("job_description", "")
    company_name = state.get("company_name", "Not found")

    whois_data = evidence.get("whois", {})
    website_data = evidence.get("website", {})
    online_reputation_data = evidence.get("online_reputation", {})

    try:
        settings = get_settings()

        llm = get_gemini_llm_with_fallbacks(temperature=0.1)

        prompt = REASONING_PROMPT.format(
            job_description_preview=job_description[:500],
            company_name=company_name or "Not found",
            whois_data=json.dumps(whois_data, indent=2),
            website_data=json.dumps(website_data, indent=2),
            online_reputation_data=json.dumps(online_reputation_data, indent=2),
        )

        messages = [
            SystemMessage(
                content="You are a fraud detection expert. Analyze evidence "
                "and return structured JSON assessments."
            ),
            HumanMessage(content=prompt),
        ]

        logger.info("[Gemini] Sending reasoning request...")
        response = llm.invoke(messages)
        logger.info("[Gemini] Reasoning response received")

        reasoning_result = parse_json_response(response.content)
        if not reasoning_result:
            logger.warning("[Gemini Reasoning] Could not parse JSON response, using defaults")
            reasoning_result = {"risk_score": 0.5, "fraud_verdict": "suspicious", "reasoning": "Unable to parse AI response"}

        updated_state["gemini_reasoning"] = reasoning_result.get("reasoning", "")
        updated_state["agent_risk_score"] = float(
            reasoning_result.get("risk_score", 0.5)
        )
        updated_state["agent_verdict"] = reasoning_result.get(
            "fraud_verdict", "suspicious"
        )

        evidence["gemini"] = reasoning_result
        updated_state["investigation_evidence"] = evidence

        logger.info(
            "[Gemini Reasoning] Completed: verdict=%s, risk_score=%s",
            updated_state["agent_verdict"],
            updated_state["agent_risk_score"],
        )

    except Exception as exception:
        logger.exception("[Gemini Reasoning] Failed: %s", str(exception))
        updated_state["gemini_reasoning"] = f"AI reasoning unavailable: {str(exception)}"
        updated_state["agent_risk_score"] = 0.5
        updated_state["agent_verdict"] = "suspicious"

    logger.info("[Gemini Reasoning] Completed")
    return updated_state

