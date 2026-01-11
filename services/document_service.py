import uuid
from typing import List
from datetime import datetime

from models import Document, DocumentInput, QueryResult, RetrievedDocument
from repositories.vector_store import VectorStoreRepository
from services.embedding_service import EmbeddingService
from exceptions import DocumentNotFoundError

class DocumentService:
    """Service for document operations"""

    def __init__(self, vector_store: VectorStoreRepository, embedding_service: EmbeddingService):
        self.vector_store = vector_store
        self.embedding_service = embedding_service

    def ingest_document(self, doc_input: DocumentInput) -> str:
        """Ingest a new document"""
        # Generate embedding
        embedding = self.embedding_service.generate_embedding(doc_input.content)

        # Create document
        now = datetime.now()
        document = Document(
            id=str(uuid.uuid4()),
            content=doc_input.content,
            metadata=doc_input.metadata,
            embedding=embedding,
            created_at=now,
            updated_at=now
        )

        # Store in vector store
        return self.vector_store.store_document(document)

    def query_documents(self, query: str, top_k: int = 5) -> QueryResult:
        """Query documents and generate answer"""
        import time
        start_time = time.time()

        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)

        # Search similar documents
        retrieved_docs = self.vector_store.search_similar(query_embedding, top_k)

        # Generate simple answer (in real app, this would use LLM)
        if retrieved_docs:
            top_doc = retrieved_docs[0]
            answer = f"Based on the most relevant document: {top_doc.content[:200]}..."
        else:
            answer = "No relevant documents found."

        processing_time = time.time() - start_time

        return QueryResult(
            query=query,
            documents=retrieved_docs,
            answer=answer,
            processing_time=processing_time
        )

    def get_document(self, doc_id: str) -> Document:
        """Get a document by ID"""
        document = self.vector_store.get_document(doc_id)
        if not document:
            raise DocumentNotFoundError(f"Document with ID {doc_id} not found")
        return document

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID"""
        # Check if document exists first
        self.get_document(doc_id)  # This will raise if not found
        return self.vector_store.delete_document(doc_id)

    def list_documents(self, limit: int = 10) -> List[Document]:
        """List documents"""
        return self.vector_store.list_documents(limit)

    def count_documents(self) -> int:
        """Count total documents"""
        return self.vector_store.count_documents()

    def batch_ingest(self, documents: List[DocumentInput]) -> List[dict]:
        """Batch ingest multiple documents"""
        results = []
        for doc in documents:
            try:
                doc_id = self.ingest_document(doc)
                results.append({"id": doc_id, "status": "success"})
            except Exception as e:
                results.append({"status": "error", "error": str(e)})
        return results
