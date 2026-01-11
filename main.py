#!/usr/bin/env python3
"""
Refactored BitHealth API - Clean Architecture Implementation

This is a refactored version of the original messy codebase that demonstrates
proper software engineering practices including:
- Dependency injection
- Separation of concerns
- Clean architecture layers
- Proper error handling
- Configuration management
- Testable design
"""

import uvicorn
from .config import settings
from .api import app

if __name__ == "__main__":
    uvicorn.run(
        "bithealth.api:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
