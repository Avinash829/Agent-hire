"""
Dependency Injection Container.

Provides centralized access to application services and
components for dependency injection into route handlers.
"""

from app.ml.pipeline import MLPipeline
from app.services.verification_service import VerificationService
from app.services.synthesis_service import SynthesisService
from app.services.agent_service import AgentService
from app.services.history_service import HistoryService
from app.repositories.verification_repository import VerificationRepository
from app.logging.logger import get_logger

logger = get_logger(__name__)


class ServiceContainer:
    """
    Dependency injection container that manages service instances.

    Ensures singleton instances of stateless services and allows
    overriding for testing.
    """

    def __init__(self):
        self._ml_pipeline = None
        self._synthesis_service = None
        self._agent_service = None
        self._verification_service = None
        self._history_service = None
        self._repository = None

    def get_ml_pipeline(self) -> MLPipeline:
        """Return ML pipeline singleton instance."""
        if self._ml_pipeline is None:
            self._ml_pipeline = MLPipeline()
        return self._ml_pipeline

    def get_synthesis_service(self) -> SynthesisService:
        """Return synthesis service singleton instance."""
        if self._synthesis_service is None:
            self._synthesis_service = SynthesisService()
        return self._synthesis_service

    def get_agent_service(self) -> AgentService:
        """Return agent service singleton instance."""
        if self._agent_service is None:
            self._agent_service = AgentService()
        return self._agent_service

    def get_repository(self) -> VerificationRepository:
        """Return repository singleton instance."""
        if self._repository is None:
            self._repository = VerificationRepository()
        return self._repository

    def get_verification_service(self) -> VerificationService:
        """Return verification service singleton instance."""
        if self._verification_service is None:
            self._verification_service = VerificationService(
                ml_pipeline=self.get_ml_pipeline(),
                agent_service=self.get_agent_service(),
                synthesis_service=self.get_synthesis_service(),
                repository=self.get_repository(),
            )
        return self._verification_service

    def get_history_service(self) -> HistoryService:
        """Return history service singleton instance."""
        if self._history_service is None:
            self._history_service = HistoryService(
                repository=self.get_repository()
            )
        return self._history_service


_container = ServiceContainer()


def get_container() -> ServiceContainer:
    """Return the global service container instance."""
    return _container

