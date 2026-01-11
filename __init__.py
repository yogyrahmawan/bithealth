"""
BitHealth API - Clean Architecture Implementation

A refactored document retrieval and Q&A API built with FastAPI, LangGraph, and Qdrant.
Demonstrates clean software engineering practices including dependency injection,
service layer pattern, and proper separation of concerns.
"""

__version__ = "1.0.0"
__author__ = "BitHealth Team"
__description__ = "Document retrieval and Q&A API with clean architecture"

# Package-level imports for convenience
try:
    from .config import settings
    from .api import app
    from .container import Container

    # Make key components easily accessible
    __all__ = [
        "app",           # FastAPI application instance
        "settings",      # Application configuration
        "Container",     # Dependency injection container
        "__version__",
        "__author__",
        "__description__"
    ]

except ImportError:
    # Handle case where imports fail (e.g., missing dependencies)
    __all__ = ["__version__", "__author__", "__description__"]
    app = None
    settings = None
    Container = None
