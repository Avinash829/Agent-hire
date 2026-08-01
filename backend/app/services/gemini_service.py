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
from dataclasses import dataclass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)

# Ordered list of active Gemini models for automatic fallback.
# Active stable models are placed first to avoid deprecation 404s.
GEMINI_MODELS: List[str] = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
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
    - Automatic model fallback chain when one model is unavailable or quota-exceeded
    - Retry logic with exponential backoff for transient failures
    - Safe handling of string or multimodal list responses from LangChain
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

                    # Model-not-found (404) or Quota Exceeded (429): jump to next model immediately
                    if ("404" in error_lower and "model" in error_lower) or (
                        "429" in error_lower or "resource_exhausted" in error_lower or "quota" in error_lower
                    ):
                        logger.warning(
                            "Model %s failed with quota/availability issue (%s), switching to next model in chain",
                            model_name,
                            "429 Quota" if "429" in error_lower or "quota" in error_lower else "404 Not Found",
                        )
                        break  # inner retry loop -> outer model fallback loop

                    # Non-retryable (auth, invalid request)
                    if self._is_non_retryable(error_lower):
                        logger.error(
                            "Non-retryable error on %s: %s",
                            model_name,
                            last_error[:200],
                        )
                        break  # skip retries for this model, try next model in chain

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

        # All models x retries exhausted
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
            "max_retries": 1,  # Prevent LangChain internal duplicate retries
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        return ChatGoogleGenerativeAI(**kwargs)

    @staticmethod
    def _clean_response(content: Any) -> str:
        """Safely extract text and strip markdown JSON fences from response content."""
        if not content:
            return ""

        # Handle LangChain list-based output format
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
                elif isinstance(part, str):
                    text_parts.append(part)
            content = "".join(text_parts)
        elif not isinstance(content, str):
            content = str(content)

        cleaned = content.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        return cleaned.strip()

    @staticmethod
    def _is_non_retryable(error_lower: str) -> bool:
        """Return True if the error should NOT be retried on the same model."""
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