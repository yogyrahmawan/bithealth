class BitHealthException(Exception):
    """Base exception for BitHealth application"""
    pass

class DocumentNotFoundError(BitHealthException):
    """Raised when a document is not found"""
    pass

class EmbeddingError(BitHealthException):
    """Raised when embedding generation fails"""
    pass

class VectorStoreError(BitHealthException):
    """Raised when vector store operations fail"""
    pass

class WorkflowError(BitHealthException):
    """Raised when workflow execution fails"""
    pass

class ConfigurationError(BitHealthException):
    """Raised when configuration is invalid"""
    pass
