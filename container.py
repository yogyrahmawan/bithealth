from config import settings
from repositories.vector_store import QdrantRepository
from services.embedding_service import EmbeddingService
from services.document_service import DocumentService
from services.workflow_service import WorkflowService

class Container:
    """Dependency injection container"""

    def __init__(self):
        self._services = {}
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all services"""
        # Infrastructure layer
        self._services['vector_store'] = QdrantRepository(
            url=settings.qdrant_url,
            collection_name=settings.collection_name,
            embedding_dim=settings.embedding_dim
        )

        # Domain services
        self._services['embedding_service'] = EmbeddingService(
            dimension=settings.embedding_dim
        )

        # Application services
        self._services['document_service'] = DocumentService(
            vector_store=self._services['vector_store'],
            embedding_service=self._services['embedding_service']
        )

        self._services['workflow_service'] = WorkflowService(
            document_service=self._services['document_service']
        )

    def get(self, service_name: str):
        """Get a service by name"""
        if service_name not in self._services:
            raise ValueError(f"Service {service_name} not found")
        return self._services[service_name]

    # Convenience properties
    @property
    def document_service(self) -> DocumentService:
        return self.get('document_service')

    @property
    def workflow_service(self) -> WorkflowService:
        return self.get('workflow_service')

    @property
    def vector_store(self):
        return self.get('vector_store')
