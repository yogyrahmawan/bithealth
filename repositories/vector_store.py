from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from models import Document, RetrievedDocument, DocumentInput
from exceptions import VectorStoreError, DocumentNotFoundError

class VectorStoreRepository(ABC):
    """Abstract base class for vector store operations"""

    @abstractmethod
    def store_document(self, document: Document) -> str:
        """Store a document in the vector store"""
        pass

    @abstractmethod
    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[RetrievedDocument]:
        """Search for similar documents by embedding"""
        pass

    @abstractmethod
    def get_document(self, doc_id: str) -> Optional[Document]:
        """Retrieve a document by ID"""
        pass

    @abstractmethod
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID"""
        pass

    @abstractmethod
    def list_documents(self, limit: int = 10) -> List[Document]:
        """List documents with pagination"""
        pass

    @abstractmethod
    def count_documents(self) -> int:
        """Count total documents"""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if vector store is healthy"""
        pass

class QdrantRepository(VectorStoreRepository):
    """Qdrant implementation of vector store repository"""

    def __init__(self, url: str, collection_name: str, embedding_dim: int):
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim

        try:
            self.client = QdrantClient(url=url)
            self._ensure_collection_exists()
        except Exception as e:
            raise VectorStoreError(f"Failed to connect to Qdrant: {str(e)}")

    def _ensure_collection_exists(self):
        """Ensure the collection exists, create if it doesn't"""
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE
                    )
                )
            except Exception as e:
                if "already exists" not in str(e).lower():
                    raise VectorStoreError(f"Failed to create collection: {str(e)}")

    def store_document(self, document: Document) -> str:
        """Store a document in Qdrant"""
        try:
            if not document.embedding:
                raise VectorStoreError("Document must have embedding")

            payload = {
                "content": document.content,
                "metadata": document.metadata or {},
                "created_at": document.created_at.isoformat(),
                "updated_at": document.updated_at.isoformat()
            }

            self.client.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(
                    id=document.id,
                    vector=document.embedding,
                    payload=payload
                )]
            )
            return document.id
        except Exception as e:
            raise VectorStoreError(f"Failed to store document: {str(e)}")

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[RetrievedDocument]:
        """Search for similar documents"""
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            results = []
            for hit in search_result:
                results.append(RetrievedDocument(
                    id=hit.id,
                    content=hit.payload.get("content", ""),
                    metadata=hit.payload.get("metadata", {}),
                    score=hit.score
                ))
            return results
        except Exception as e:
            raise VectorStoreError(f"Failed to search documents: {str(e)}")

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Retrieve a document by ID"""
        try:
            # Qdrant doesn't have direct get by ID, so we use scroll with filter
            points = self.client.scroll(
                collection_name=self.collection_name,
                limit=1,
                scroll_filter={
                    "must": [{"key": "id", "match": {"value": doc_id}}]
                }
            )[0]

            if not points:
                return None

            point = points[0]
            return Document(
                id=point.id,
                content=point.payload.get("content", ""),
                metadata=point.payload.get("metadata", {}),
                embedding=point.vector,
                created_at=datetime.fromisoformat(point.payload.get("created_at")),
                updated_at=datetime.fromisoformat(point.payload.get("updated_at"))
            )
        except Exception as e:
            raise VectorStoreError(f"Failed to get document: {str(e)}")

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[doc_id]
            )
            return True
        except Exception as e:
            raise VectorStoreError(f"Failed to delete document: {str(e)}")

    def list_documents(self, limit: int = 10) -> List[Document]:
        """List documents with pagination"""
        try:
            points = self.client.scroll(
                collection_name=self.collection_name,
                limit=limit
            )[0]

            documents = []
            for point in points:
                documents.append(Document(
                    id=point.id,
                    content=point.payload.get("content", ""),
                    metadata=point.payload.get("metadata", {}),
                    embedding=point.vector,
                    created_at=datetime.fromisoformat(point.payload.get("created_at", datetime.now().isoformat())),
                    updated_at=datetime.fromisoformat(point.payload.get("updated_at", datetime.now().isoformat()))
                ))
            return documents
        except Exception as e:
            raise VectorStoreError(f"Failed to list documents: {str(e)}")

    def count_documents(self) -> int:
        """Count total documents"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            raise VectorStoreError(f"Failed to count documents: {str(e)}")

    def health_check(self) -> bool:
        """Check if Qdrant is healthy"""
        try:
            self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False
