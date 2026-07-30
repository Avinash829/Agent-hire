"""
Retry Utility Module.

Provides configurable retry logic with exponential backoff for
external service calls (Gemini, Tavily, WHOIS, HTTP requests).

Retries only transient/retryable failures.
Does NOT retry authentication, authorization, or invalid-request errors.
"""

import asyncio
import time
from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Awaitable,
    Union,
    Tuple,
)
from functools import wraps
from app.logging.logger import get_logger

logger = get_logger(__name__)

# Default configuration
DEFAULT_MAX_RETRIES: int = 3
DEFAULT_BASE_DELAY: float = 1.0
DEFAULT_MAX_DELAY: float = 15.0
DEFAULT_BACKOFF_FACTOR: float = 2.0

# Fragments that indicate a non-retryable error.
NON_RETRYABLE_FRAGMENTS: Tuple[str, ...] = (
    # Authentication / authorisation
    "api_key_invalid",
    "api key not valid",
    "invalid_api_key",
    "invalid api key",
    "permission denied",
    "permission_denied",
    "auth error",
    "unauthorized",
    "not authenticated",
    "authentication failed",
    "access denied",
    # Invalid input
    "invalid request",
    "bad request",
    "invalid argument",
    "invalid parameter",
    # Not found / model not found
    "404",
    "not found",
    # Rate limiting (these *are* retryable, but we detect via status code
    # or separate handling; the fragments below are NOT retryable)
    "does not exist",
    "not supported",
    "model not found",
)

# Fragments that ARE retryable (transient failures)
RETRYABLE_FRAGMENTS: Tuple[str, ...] = (
    "timeout",
    "time out",
    "connection",
    "connection refused",
    "connection reset",
    "connection error",
    "reset by peer",
    "broken pipe",
    "service unavailable",
    "503",
    "502",
    "504",
    "429",
    "too many requests",
    "rate limit",
    "rate_limit",
    "internal server error",
    "500",
    "temporarily unavailable",
    "server error",
    "gateway timeout",
    "upstream",
    "deadline exceeded",
    "cancelled",
)


def is_retryable_error(exception: Exception) -> bool:
    """
    Determine whether an exception represents a transient/retryable error.

    Args:
        exception: The exception to check.

    Returns:
        True if the error is retryable, False otherwise.
    """
    error_msg = str(exception).lower()

    # First check for explicit non-retryable signals
    for fragment in NON_RETRYABLE_FRAGMENTS:
        if fragment in error_msg:
            logger.debug("Non-retryable error detected: %s", fragment)
            return False

    # Then check for retryable signals
    for fragment in RETRYABLE_FRAGMENTS:
        if fragment in error_msg:
            logger.debug("Retryable error detected: %s", fragment)
            return True

    # By default, consider unknown errors as non-retryable
    # to avoid infinite retry loops on unexpected errors.
    return False


# ------------------------------------------------------------------
# Synchronous retry
# ------------------------------------------------------------------

def retry(
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_delay: float = DEFAULT_BASE_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    retryable_exceptions: Optional[Tuple[type, ...]] = None,
):
    """
    Decorator for synchronous functions with exponential backoff retry.

    Only retries when the exception is classified as retryable.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds.
        max_delay: Maximum delay in seconds.
        backoff_factor: Multiplier for successive delays.
        retryable_exceptions: If provided, only retry these exception types.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc

                    if attempt >= max_retries:
                        logger.warning(
                            "Retry exhausted | func=%s attempts=%d error=%s",
                            func.__name__,
                            attempt,
                            str(exc)[:200],
                        )
                        raise

                    # Check exception type filter
                    if retryable_exceptions is not None and not isinstance(
                        exc, retryable_exceptions
                    ):
                        raise

                    # Check if this error is retryable
                    if not is_retryable_error(exc):
                        raise

                    delay = min(base_delay * (backoff_factor**attempt), max_delay)

                    logger.info(
                        "Retrying | func=%s attempt=%d/%d delay=%.1fs error=%s",
                        func.__name__,
                        attempt + 1,
                        max_retries,
                        delay,
                        str(exc)[:150],
                    )

                    time.sleep(delay)

            # Should not reach here, but just in case
            if last_exception:
                raise last_exception
            return None

        return wrapper

    return decorator


# ------------------------------------------------------------------
# Asynchronous retry
# ------------------------------------------------------------------

def retry_async(
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_delay: float = DEFAULT_BASE_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    retryable_exceptions: Optional[Tuple[type, ...]] = None,
):
    """
    Decorator for async functions with exponential backoff retry.

    Only retries when the exception is classified as retryable.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds.
        max_delay: Maximum delay in seconds.
        backoff_factor: Multiplier for successive delays.
        retryable_exceptions: If provided, only retry these exception types.
    """
    def decorator(
        func: Callable[..., Awaitable[Any]]
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc

                    if attempt >= max_retries:
                        logger.warning(
                            "Async retry exhausted | func=%s attempts=%d error=%s",
                            func.__name__,
                            attempt,
                            str(exc)[:200],
                        )
                        raise

                    # Check exception type filter
                    if retryable_exceptions is not None and not isinstance(
                        exc, retryable_exceptions
                    ):
                        raise

                    # Check if this error is retryable
                    if not is_retryable_error(exc):
                        raise

                    delay = min(base_delay * (backoff_factor**attempt), max_delay)

                    logger.info(
                        "Async retrying | func=%s attempt=%d/%d delay=%.1fs "
                        "error=%s",
                        func.__name__,
                        attempt + 1,
                        max_retries,
                        delay,
                        str(exc)[:150],
                    )

                    await asyncio.sleep(delay)

            # Should not reach here, but just in case
            if last_exception:
                raise last_exception
            return None

        return wrapper

    return decorator

