from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Settings
    app_name: str = "BitHealth API"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8002

    # Qdrant Settings
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "documents"
    embedding_dim: int = 384

    # LangGraph Settings
    max_retrieval_results: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
