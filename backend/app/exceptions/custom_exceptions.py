"""
Custom Exception Classes for the Application.

Defines domain-specific exceptions with consistent error codes
and messages for proper error handling throughout the application.
"""


class ApplicationError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=401, error_code="AUTHENTICATION_ERROR")


class AuthorizationError(ApplicationError):
    """Raised when user is not authorized to perform an action."""

    def __init__(self, message: str = "Not authorized"):
        super().__init__(message=message, status_code=403, error_code="AUTHORIZATION_ERROR")


class ValidationError(ApplicationError):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message=message, status_code=422, error_code="VALIDATION_ERROR")


class NotFoundError(ApplicationError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404, error_code="NOT_FOUND")


class MLPipelineError(ApplicationError):
    """Raised when the ML pipeline encounters an error."""

    def __init__(self, message: str = "ML pipeline error"):
        super().__init__(message=message, status_code=500, error_code="ML_PIPELINE_ERROR")


class AgentPipelineError(ApplicationError):
    """Raised when the LangGraph agent pipeline encounters an error."""

    def __init__(self, message: str = "Agent pipeline error"):
        super().__init__(message=message, status_code=500, error_code="AGENT_PIPELINE_ERROR")


class DatabaseError(ApplicationError):
    """Raised when a database operation fails."""

    def __init__(self, message: str = "Database error"):
        super().__init__(message=message, status_code=500, error_code="DATABASE_ERROR")


class ExternalServiceError(ApplicationError):
    """Raised when an external service (WHOIS, Tavily, etc.) fails."""

    def __init__(self, message: str = "External service error"):
        super().__init__(message=message, status_code=502, error_code="EXTERNAL_SERVICE_ERROR")

