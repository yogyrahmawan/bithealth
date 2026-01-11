# BitHealth API - Clean Architecture Implementation

A refactored document retrieval and Q&A API built with FastAPI, LangGraph, and Qdrant. This project demonstrates clean software engineering practices including dependency injection, service layer pattern, and proper separation of concerns.

## ✨ Features

- 🔍 **Document Ingestion**: Store and index documents with metadata
- ❓ **Intelligent Q&A**: Query documents using natural language with LangGraph workflows
- 🏗️ **Clean Architecture**: Well-structured codebase with proper separation of concerns
- 🧪 **Dependency Injection**: Service locator pattern for testable components
- 📊 **Health Monitoring**: Comprehensive health checks and debug endpoints
- 🐳 **Docker Ready**: Easy deployment with containerization

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (for Qdrant vector database)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bithealth
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Qdrant database**
   ```bash
   docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

5. **Run the application**
   ```bash
   # Development mode
   uvicorn bithealth.api:app --reload --host 0.0.0.0 --port 8000

   # Production mode
   uvicorn bithealth.api:app --host 0.0.0.0 --port 8000
   ```

## 📡 API Endpoints

### Health & Monitoring
- `GET /health` - Health check
- `GET /debug/config` - Show configuration
- `GET /debug/services` - Show service status

### Document Operations
- `POST /ingest` - Ingest a document
- `POST /query` - Query documents
- `GET /documents` - List documents
- `DELETE /documents/{doc_id}` - Delete document
- `POST /batch_ingest` - Batch document ingestion

## 💡 API Examples

### Ingest a Document
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a sample document about machine learning.",
    "metadata": {"category": "AI", "author": "John Doe"}
  }'
```

### Query Documents
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 3
  }'
```

### Health Check
```bash
curl http://localhost:8000/health
# Returns: {"status": "OK", "qdrant": "connected", "workflow": "ready", "documents_count": 1}
```

## 🏛️ Architecture

The application follows Clean Architecture principles:

```
bithealth/
├── api.py              # FastAPI routes & dependency injection
├── config.py           # Configuration management
├── container.py        # Dependency injection container
├── models.py           # Domain models & DTOs
├── exceptions.py       # Custom exceptions
├── services/           # Business logic layer
│   ├── document_service.py
│   ├── embedding_service.py
│   └── workflow_service.py
└── repositories/       # Data access layer
    └── vector_store.py
```

### Key Design Patterns

- **Dependency Injection**: Service locator pattern
- **Repository Pattern**: Abstract data access
- **Service Layer**: Business logic orchestration
- **Clean Architecture**: Clear separation of concerns

## ⚙️ Configuration

Create a `.env` file to override default settings:

```env
# API Settings
APP_NAME=BitHealth API
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

# Qdrant Settings
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=documents
EMBEDDING_DIM=384

# LangGraph Settings
MAX_RETRIEVAL_RESULTS=5
```

## 🧪 Development

### Running Tests
```bash
# Add tests in the future
pytest
```

### Code Quality
```bash
# Add linting and formatting in the future
black .
flake8 .
```

### Docker Deployment
```bash
# Build and run with Docker (add Dockerfile first)
docker build -t bithealth .
docker run -p 8000:8000 bithealth
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Vector search powered by [Qdrant](https://qdrant.tech/)
- Workflow orchestration with [LangGraph](https://github.com/langchain-ai/langgraph)

---

## 📚 Original Exercise Context

This codebase was originally an onboarding exercise that deliberately omitted key engineering practices to evaluate design instincts. The original README focused on identifying architectural issues and planning improvements.

**What was improved:**
- ✅ Eliminated global state management
- ✅ Introduced dependency injection
- ✅ Separated concerns with service/repository layers
- ✅ Added proper configuration management
- ✅ Implemented comprehensive error handling
- ✅ Enabled unit testability
- ✅ Created extensible architecture for future changes

The refactored code now demonstrates production-ready software engineering practices! 🚀 