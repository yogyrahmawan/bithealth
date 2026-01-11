import logging
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from config import settings
from container import Container
from models import (
    DocumentInput, QueryInput, QueryResult,
    Document, HealthStatus
)
from exceptions import BitHealthException, DocumentNotFoundError
from services.document_service import DocumentService
from services.workflow_service import WorkflowService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Refactored BitHealth API with clean architecture"
)

# Global container instance - will be initialized on startup
container = None

# Startup event to initialize container
@app.on_event("startup")
async def startup_event():
    """Initialize the dependency injection container on startup"""
    global container
    container = Container()
    logger.info("Dependency injection container initialized")

# Dependency functions
def get_document_service() -> DocumentService:
    if container is None:
        raise RuntimeError("Container not initialized")
    return container.document_service

def get_workflow_service() -> WorkflowService:
    if container is None:
        raise RuntimeError("Container not initialized")
    return container.workflow_service

# Exception handlers
@app.exception_handler(BitHealthException)
async def bithealth_exception_handler(request, exc: BitHealthException):
    logger.error(f"BitHealth error: {str(exc)}")
    return {"error": str(exc)}, 400

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return {"error": "Internal server error"}, 500

# Routes
@app.post("/ingest", response_model=dict)
async def ingest_document(
    doc: DocumentInput,
    service: DocumentService = Depends(get_document_service)
):
    """Ingest a new document"""
    try:
        doc_id = service.ingest_document(doc)
        return {"id": doc_id, "message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/query", response_model=QueryResult)
async def query_documents(
    query_input: QueryInput,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Query documents using workflow"""
    try:
        result = workflow_service.execute_query(query_input.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/documents", response_model=List[Document])
async def list_documents(
    limit: int = 10,
    service: DocumentService = Depends(get_document_service)
):
    """List documents"""
    try:
        return service.list_documents(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@app.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    service: DocumentService = Depends(get_document_service)
):
    """Delete a document by ID"""
    try:
        service.delete_document(doc_id)
        return {"message": f"Document {doc_id} deleted successfully"}
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

@app.get("/health", response_model=HealthStatus)
async def health_check(
    service: DocumentService = Depends(get_document_service),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Health check endpoint"""
    try:
        qdrant_healthy = container.vector_store.health_check()
        workflow_healthy = workflow_service.is_healthy()
        documents_count = service.count_documents()

        status = "healthy" if qdrant_healthy and workflow_healthy else "unhealthy"

        return HealthStatus(
            status="OK" if status == "healthy" else status,
            qdrant="connected" if qdrant_healthy else "disconnected",
            workflow="ready" if workflow_healthy else "not ready",
            documents_count=documents_count
        )
    except Exception as e:
        return HealthStatus(
            status="unhealthy",
            qdrant="error",
            workflow="error",
            documents_count=0
        )

@app.post("/batch_ingest", response_model=List[dict])
async def batch_ingest(
    documents: List[DocumentInput],
    service: DocumentService = Depends(get_document_service)
):
    """Batch ingest multiple documents"""
    try:
        return service.batch_ingest(documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch ingestion failed: {str(e)}")

# Debug endpoints
@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to show current configuration"""
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "qdrant_url": settings.qdrant_url,
        "collection_name": settings.collection_name,
        "embedding_dim": settings.embedding_dim,
        "max_retrieval_results": settings.max_retrieval_results
    }

@app.get("/debug/services")
async def debug_services():
    """Debug endpoint to show service status"""
    if container is None:
        return {"error": "Container not initialized"}
    return {
        "vector_store_healthy": container.vector_store.health_check(),
        "workflow_ready": container.workflow_service.is_healthy(),
        "documents_count": container.document_service.count_documents()
    }
