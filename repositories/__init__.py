"""
Repositories Layer - Data Access Components

This package contains repository classes that abstract data access operations.
Repositories provide a clean interface for interacting with external data sources
like databases, vector stores, and external APIs.
"""

from .vector_store import VectorStoreRepository, QdrantRepository

__all__ = [
    "VectorStoreRepository",
    "QdrantRepository"
]
