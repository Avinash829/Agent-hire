"""
Centralized Gemini Model Manager.

Provides a single point of configuration for Gemini LLM models
with automatic fallback, retry logic, and structured error handling.

Every LangChain/Gemini node must use this manager.
No hardcoded model names anywhere else in the codebase.
"""

import json
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import BaseMessage
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)

# Ordered list of Gemini models for automatic fallback.
# If one returns 404/model not found, the next is tried.
GEMINI_MODELS: List[str] = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "gemini-1.0-pro",
]

# Retry configuration
MAX_RETRIES: int = 3
RETRY_BASE_DELAY: float = 1.0
RETRY_MAX_DELAY: float = 10.0

# Non-retryable error fragments (authentication, invalid requests, etc.)
NON_RETRYABLE_FRAGMENTS: List[str] = [
    "api_key_invalid",
    "api key not valid",
    "invalid_api_key",
    "permission denied",
    "permission_denied",
    "auth error",
    "unauthorized",
    "not authenticated",
]


@dataclass
class GeminiResponse:
    """Structured response from a Gemini model invocation."""

    success: bool
    content: Optional[str] = None
    model_used: Optional[str] = None
    error: Optional[str] = None
    retries_attempted: int = 0
    fallback_used: bool = False
    duration_ms: float = 0.0


class GeminiManager:
    """
    Centralized manager for Gemini LLM interactions.

    Features:
    - Automatic model fallback chain when one model is unavailable
    - Retry logic with exponential backoff for transient failures
    - Structured error responses (never raises exceptions to caller)
    - Detailed logging of model used, fallbacks, retries, and duration
    """

    def __init__(
        self,
        models: Optional[List[str]] = None,
        max_retries: int = MAX_RETRIES,
        retry_base_delay: float = RETRY_BASE_DELAY,
        retry_max_delay: float = RETRY_MAX_DELAY,
    ):
        self.settings = get_settings()
        self.api_key = self.settings.gemini_api_key
        self.models = models or GEMINI_MODELS
        self.max_retries = max_retries
        self.retry_base_delay = retry_base_delay
        self.retry_max_delay = retry_max_delay

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def invoke(
        self,
        messages: List[BaseMessage],
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> GeminiResponse:
        """
        Invoke Gemini with automatic fallback and retry.

        Args:
            messages: LangChain message list.
            temperature: Sampling temperature.
            max_tokens: Maximum output tokens.

        Returns:
            GeminiResponse with content or structured error.
        """
        start_time = time.monotonic()
        first_model: Optional[str] = None
        last_error: Optional[str] = None

        for model_idx, model_name in enumerate(self.models):
            if first_model is None:
                first_model = model_name

            llm = self._build_llm(model_name, temperature, max_tokens)

            for attempt in range(self.max_retries):
                try:
                    logger.info(
                        "Gemini call | model=%s attempt=%d/%d",
                        model_name,
                        attempt + 1,
                        self.max_retries,
                    )

                    response = llm.invoke(messages)
                    cleaned = self._clean_response(response.content)

                    elapsed = (time.monotonic() - start_time) * 1000
                    logger.info(
                        "Gemini success | model=%s attempt=%d/%d "
                        "fallback=%s duration=%.0fms",
                        model_name,
                        attempt + 1,
                        self.max_retries,
                        "yes" if model_idx > 0 else "no",
                        elapsed,
                    )

                    return GeminiResponse(
                        success=True,
                        content=cleaned,
                        model_used=model_name,
                        retries_attempted=attempt,
                        fallback_used=model_idx > 0,
                        duration_ms=elapsed,
                    )

                except Exception as exc:
                    last_error = str(exc)
                    error_lower = last_error.lower()

                    # Model-not-found: jump to next model immediately
                    if "404" in error_lower and "model" in error_lower:
                        logger.warning(
                            "Model %s not found (404), "
                            "switching to next model",
                            model_name,
                        )
                        break  # inner retry loop → outer model loop

                    # Non-retryable (auth, invalid request, …)
                    if self._is_non_retryable(error_lower):
                        logger.error(
                            "Non-retryable error on %s: %s",
                            model_name,
                            last_error[:200],
                        )
                        break  # skip retries for this model, try next

                    # Retryable transient failure
                    if attempt < self.max_retries - 1:
                        delay = min(
                            self.retry_base_delay * (2**attempt),
                            self.retry_max_delay,
                        )
                        logger.warning(
                            "Gemini retry | model=%s attempt=%d/%d "
                            "delay=%.1fs error=%s",
                            model_name,
                            attempt + 2,
                            self.max_retries,
                            delay,
                            last_error[:150],
                        )
                        time.sleep(delay)
                    # else: last attempt exhausted, try next model

        # All models × retries exhausted
        elapsed = (time.monotonic() - start_time) * 1000
        logger.error(
            "All Gemini models exhausted | models=%s last_error=%s "
            "duration=%.0fms",
            self.models,
            (last_error or "unknown")[:200],
            elapsed,
        )

        return GeminiResponse(
            success=False,
            error=last_error or "All Gemini models unavailable",
            model_used=first_model,
            retries_attempted=self.max_retries,
            fallback_used=True,
            duration_ms=elapsed,
        )

    def invoke_structured(
        self,
        messages: List[BaseMessage],
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Invoke Gemini and parse the response as JSON.

        Returns a dict that always contains at least ``status``:
        - ``"success"`` when parsing succeeds.
        - ``"error"`` when the call or parsing fails.

        Never raises.
        """
        result = self.invoke(messages, temperature, max_tokens)

        if not result.success or not result.content:
            return {
                "status": "error",
                "error": result.error or "No response from Gemini",
                "model_used": result.model_used,
                "fallback_used": result.fallback_used,
            }

        try:
            parsed = json.loads(result.content)
            if not isinstance(parsed, dict):
                raise ValueError("Response is not a JSON object")
            parsed["status"] = "success"
            parsed["model_used"] = result.model_used
            parsed["fallback_used"] = result.fallback_used
            return parsed
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Failed to parse Gemini JSON: %s", exc)
            return {
                "status": "error",
                "error": f"Failed to parse AI response: {exc}",
                "model_used": result.model_used,
                "fallback_used": result.fallback_used,
                "raw_content": (result.content or "")[:500],
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_llm(
        self,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
    ) -> ChatGoogleGenerativeAI:
        kwargs: Dict[str, Any] = {
            "model": model,
            "google_api_key": self.api_key,
            "temperature": temperature,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        return ChatGoogleGenerativeAI(**kwargs)

    @staticmethod
    def _clean_response(content: str) -> str:
        """Strip markdown JSON fences from a model response."""
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()

    @staticmethod
    def _is_non_retryable(error_lower: str) -> bool:
        """Return True if the error should NOT be retried."""
        return any(f in error_lower for f in NON_RETRYABLE_FRAGMENTS)


# ------------------------------------------------------------------
# Singleton accessor
# ------------------------------------------------------------------

_gemini_manager: Optional[GeminiManager] = None


def get_gemini_manager() -> GeminiManager:
    """Return the cached GeminiManager singleton."""
    global _gemini_manager
    if _gemini_manager is None:
        _gemini_manager = GeminiManager()
    return _gemini_manager

