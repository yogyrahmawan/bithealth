from typing import List
import random
from exceptions import EmbeddingError

class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        In production, this would use a real embedding model like sentence-transformers.
        """
        if not text or not text.strip():
            raise EmbeddingError("Cannot generate embedding for empty text")

        try:
            # Fake embedding using seeded random numbers for determinism
            # In real implementation, replace with actual embedding model
            random.seed(hash(text) % (10 ** 9))
            return [random.random() for _ in range(self.dimension)]
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embedding: {str(e)}")

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        if len(embedding1) != len(embedding2):
            raise EmbeddingError("Embeddings must have same dimension")

        # Simple cosine similarity calculation
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = sum(a * a for a in embedding1) ** 0.5
        norm2 = sum(b * b for b in embedding2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
