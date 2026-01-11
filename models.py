from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

class Document(BaseModel):
    """Domain model for a document"""
    id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime

class DocumentInput(BaseModel):
    """Input model for document ingestion"""
    content: str
    metadata: Optional[Dict[str, Any]] = None

class QueryInput(BaseModel):
    """Input model for document queries"""
    query: str
    top_k: int = 5

class RetrievedDocument(BaseModel):
    """Model for retrieved documents with similarity scores"""
    id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    score: float

class QueryResult(BaseModel):
    """Result model for query operations"""
    query: str
    documents: List[RetrievedDocument]
    answer: str
    processing_time: float

class WorkflowState(BaseModel):
    """State model for LangGraph workflow"""
    query: str
    retrieved_docs: List[RetrievedDocument] = []
    final_answer: str = ""
    processing_steps: List[str] = []
    error: Optional[str] = None

class HealthStatus(BaseModel):
    """Health check response model"""
    status: str
    qdrant: str
    workflow: str
    documents_count: int
