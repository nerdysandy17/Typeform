# Help Centre API

A production-ready FastAPI application that provides intelligent document indexing and question-answering capabilities using RAG (Retrieval-Augmented Generation) with LlamaIndex, Pinecone vector database, and OpenAI embeddings.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Testing](#testing)
- [Notes](#notes)
- [Approach & Design Decisions](#approach-&-design-decisions)
- [Simplifications](#simplifications)
- [Possible Future improvements](#possible-future-improvements)
- [Use of AI](#use-of-ai)

## Overview

The Help Centre API is a RESTful service that enables intelligent search and question-answering over a corpus of help documentation. It uses vector embeddings to index documents and retrieve contextually relevant information in response to user queries.

**Key Capabilities:**
- Automatic document ingestion and vectorisation
- Semantic search across help documentation
- Context-aware question answering using RAG architecture
- Scalable vector storage with Pinecone
- Production-ready containerised deployment
- Kubernetes-ready with Helm charts

## Features

### Core Functionality
- **Document Indexing**: Automatically indexes documents from the data directory using LlamaIndex
- **Vector Storage**: Leverages Pinecone for efficient vector storage and retrieval
- **Semantic Search**: Uses OpenAI embeddings (text-embedding-ada-002) for semantic understanding
- **Question Answering**: Retrieves relevant context and synthesises answers to user queries
- **Similarity Filtering**: Configurable similarity cutoff to ensure answer quality

### API Features
- **RESTful API**: Clean, intuitive API endpoints built with FastAPI
- **Interactive Documentation**: Auto-generated Swagger UI at `/docs`
- **Health Checks**: Monitoring-ready health endpoint
- **Type Safety**: Full Pydantic model validation
- **Async Support**: Asynchronous request handling for high performance

### Operational Features
- **Containerised**: Docker support for consistent deployment
- **Environment Configuration**: Secure secrets management with `.env` files
- **Structured Logging**: Comprehensive logging for debugging and monitoring
- **Production Ready**: Configured for production deployment with proper security practices
- **Kubernetes Ready**: Complete Helm chart for orchestration (see [helm/README.md](helm/README.md))

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Routes  │ (API Endpoints)
    └────┬────┘
         │
    ┌────┴────────┐
    │   Models    │ (Request/Response)
    └────┬────────┘
         │
    ┌────┴─────────────┐
    │  Business Logic  │ (DocumentsIndexing)
    └────┬─────────────┘
         │
    ┌────┴──────────────────┐
    │  External Services    │
    │  - LlamaIndex         │
    │  - Pinecone Vector DB │
    │  - OpenAI Embeddings  │
    └───────────────────────┘
```

### RAG Pipeline Flow

1. **Document Ingestion**: Text files from `data/` are loaded using LlamaIndex
2. **Chunking**: Documents are split into manageable chunks (default: sentences)
3. **Embedding**: Each chunk is converted to a vector using OpenAI embeddings
4. **Indexing**: Vectors are stored in Pinecone for fast retrieval
5. **Query**: User questions are embedded, and similar vectors are retrieved
6. **Synthesis**: Retrieved context is used to generate accurate answers

## Technologies

### Core Framework
- **[FastAPI](https://fastapi.tiangolo.com/)** (0.124.4) - Modern, high-performance web framework
- **[Python](https://www.python.org/)** (3.12.4) - Programming language

### AI/ML Stack
- **[LlamaIndex](https://www.llamaindex.ai/)** (0.14.10) - RAG orchestration framework
- **[OpenAI](https://openai.com/)** - Embeddings and LLM capabilities
- **[Pinecone](https://www.pinecone.io/)** - Vector database for similarity search

### Configuration & Validation
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** (2.12.5) - Data validation using Python type hints
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** (1.2.1) - Environment variable management

### Deployment
- **[Docker](https://www.docker.com/)** - Containerization
- **[Kubernetes](https://kubernetes.io/)** - Container orchestration
- **[Helm](https://helm.sh/)** (3.x) - Kubernetes package management
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server (via FastAPI standard)

## Project Structure

```
help_centre_api/
├── README.md                          # This file
├── Dockerfile                         # Docker container definition
├── requirements.txt                   # Python dependencies
├── .env                              # Environment variables (not in git)
├── .helmignore                       # Helm chart ignore patterns
│
├── data/                             # Help documentation source files
│   ├── Add_a_multi-question_page_to_your_form.txt
│   ├── Create_multi-language_forms.txt
│   └── vector_store/                # Persisted vector index
│       ├── docstore.json
│       ├── graph_store.json
│       ├── image__vector_store.json
│       └── index_store.json
│
├── helm/                             # Kubernetes Helm chart
│   ├── Chart.yaml                    # Chart metadata
│   ├── values.yaml                   # Default configuration
│   ├── README.md                     # Helm deployment guide
│   └── templates/                    # Kubernetes manifests
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── secret.yaml
│       ├── hpa.yaml
│       ├── serviceaccount.yaml
│       └── _helpers.tpl
│
└── src/                              # Application source code
    ├── __init__.py
    ├── main.py                       # FastAPI application entry point
    ├── settings.py                   # Configuration management
    │
    ├── models/                       # Pydantic models
    │   ├── __init__.py
    │   ├── README.md
    │   ├── request.py                # Request schemas
    │   └── response.py               # Response schemas
    │
    ├── predict/                      # Business logic
    │   ├── __init__.py
    │   └── documents_indexing.py     # RAG implementation
    │
    └── routes/                       # API endpoints
        ├── __init__.py
        ├── documents_indexing.py     # Main query endpoint
        └── health.py                 # Health check endpoint
```

## Prerequisites

### For Local Development
- Python 3.12.4 or higher
- pip (Python package manager)
- Virtual environment tool (venv, virtualenv, or conda)

### For Docker
- Docker 20.10+
- Docker Compose (optional)

### For Kubernetes Deployment
- Kubernetes cluster (1.19+)
- Helm 3.x
- kubectl configured with cluster access

### External Services
- **OpenAI API Key**: For embeddings and LLM capabilities
- **Pinecone API Key**: For vector database storage

## Installation

### Local Setup

1. **Clone the repository** (or navigate to project directory):
   ```bash
   cd /path/to/help_centre_api
   ```

2. **Create and activate a virtual environment**:
   ```bash
   virtualenv -p python3.12 venv
   source venv/bin/activate  
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env_example .env  # If you have a template
   # Edit .env with your API keys
   ```

   Your `.env` file should contain:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

5. **Add your help documentation**:
   Place your `.txt` files in the `data/` directory.

6. **Run the application**:
   ```bash
   fastapi dev src/main.py --port 8000
   ```

7. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker build -t help-centre-api:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -p 80:80 --env-file .env help-centre-api:latest
   ```

   Or with individual environment variables:
   ```bash
   docker run -p 80:80 \
     -e OPENAI_API_KEY="your_key" \
     -e PINECONE_API_KEY="your_key" \
     help-centre-api:latest
   ```

3. **Access the API**:
   - API: http://localhost
   - Interactive docs: http://localhost/docs

## Configuration

### Environment Variables

All configuration is managed through environment variables defined in `.env`:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for embeddings | Yes | - |
| `PINECONE_API_KEY` | Pinecone API key for vector storage | Yes | - |
| `API_NAME` | Name of the API | No | `help-centre-api` |
| `API_VERSION` | Version of the API | No | `1.0.0` |
| `API_DESCRIPTION` | Description of the API | No | `help-centre-api` |
| `ENV` | Environment (dev/prod) | No | `dev` |
| `NAMESPACE` | Application namespace | No | `fastapi` |

### Application Settings

Settings are managed through `src/settings.py` using Pydantic Settings:

```python
from src.settings import settings

# Access configuration
api_key = settings.OPENAI_API_KEY
env = settings.ENV
```

### Indexing Configuration

The document indexing behaviour can be customised in `src/predict/documents_indexing.py`:

- **Top-K Results**: Change `top_k=5` in `query()` method
- **Similarity Cutoff**: Adjust `similarity_cutoff=0.4` for stricter/looser matching
- **Vector Store Path**: Modify `dir_name` in `index()` method

## Usage

### Starting the Application

**Development mode** (with auto-reload):
```bash
fastapi dev src/main.py --port 8000
```

**Production mode**:
```bash
fastapi run src/main.py --port 80 --host 0.0.0.0
```

### Making API Requests

#### Using Python

```python
import requests

# Query endpoint
response = requests.post(
    "http://localhost:8000/documents-indexing",
    json={"query": "Can I use Logic with the Multi-Question Page?"}
)

print(response.json())
# Output: {"response": "Yes, you can use Logic with the Multi-Question Page..."}
```

#### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Expand the `/documents-indexing` endpoint
3. Click "Try it out"
4. Enter your query in the request body
5. Click "Execute"

## API Documentation

### Endpoints

#### `GET /`
Root endpoint returning a welcome message.

**Response**:
```json
{
  "message": "Hello World"
}
```

#### `GET /health`
Health check endpoint for monitoring services.

**Response**:
```json
{
  "message": "Hello World"
}
```

**Status**: 200 OK

#### `POST /documents-indexing`
Main endpoint for querying the help centre documentation.

**Request Body**:
```json
{
  "query": "string"
}
```

**Parameters**:
- `query` (string, required): The question to ask about the help documentation

**Response**:
```json
{
  "response": "string"
}
```

**Example**:
```bash
POST /documents-indexing
{
  "query": "Can I add a score or create an outcome quiz with the Multi-Question Page?"
}

# Response
{
  "response": "Yes, you can create outcome quizzes with the Multi-Question Page feature..."
}
```

**Status Codes**:
- `200 OK`: Successful query
- `422 Unprocessable Entity`: Invalid request format
- `500 Internal Server Error`: Server error during processing

### Models

#### DocumentsIndexingRequest
```python
{
  "query": str  # User's question
}
```

#### DocumentsIndexingResponse
```python
{
  "response": str  # AI-generated answer based on indexed documents
}
```

## Development

### Code Structure

The codebase follows these principles:
- **Separation of Concerns**: Routes, models, and business logic are separated
- **Type Safety**: All models use Pydantic for runtime validation
- **Dependency Injection**: Settings are injected where needed
- **Async/Await**: Async endpoints for better performance

### Adding New Documents

1. Place `.txt` files in the `data/` directory
2. Delete the `data/vector_store/` directory (if it exists)
3. Restart the application - it will re-index all documents

### Logging

The application uses Python's built-in logging:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message")
```

Logs are output to stdout for Docker/Kubernetes compatibility.

## 🚢 Deployment

### Docker Deployment

The application is containerised using Docker for consistent deployment:

```dockerfile
FROM python:3.12.4-slim-bookworm
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 80
CMD ["fastapi", "run", "src/main.py", "--port", "80", "--host", "0.0.0.0"]
```

**Key features**:
- Slim Python base image for smaller size
- Dependency caching for faster rebuilds
- Binds to `0.0.0.0` for external access
- Exposes port 80 for HTTP traffic

### Kubernetes Deployment

The application includes a complete Helm chart for Kubernetes deployment with:
- High availability (2 replicas)
- Health checks and readiness probes
- Resource limits and requests
- Horizontal Pod Autoscaler (optional)
- Ingress for external access
- Secret management for API keys

For detailed Kubernetes deployment instructions, see [helm/README.md](helm/README.md).

**Quick start**:
```bash
# Install with Helm
helm install help-centre-api ./helm --namespace help-centre-api --create-namespace

# Check status
kubectl get pods -n help-centre-api

# Access logs
kubectl logs -f deployment/help-centre-api -n help-centre-api
```

### Environment-Specific Configuration

**Development**:
- Use `fastapi dev` for auto-reload
- Enable debug logging
- Use local .env file

**Production**:
- Use `fastapi run` for optimised performance
- Configure proper resource limits
- Use secrets management (Kubernetes Secrets, AWS Secrets Manager, etc.)
- Enable monitoring and alerting
- Use production-grade vector database settings

## Testing

### Manual Testing

**Test via interactive docs**:
   - Visit http://localhost:8000/docs
   - Try various queries

### Running the Indexing Script Directly

You can test the document indexing logic independently:

```bash
python -m src.predict.documents_indexing
```

This will run the example queries defined in the `__main__` block inside src/predict/documents_indexing.py.


## Notes

### Vector Store Persistence

The application persists the vector index in `data/vector_store/`. On first run:
- Documents are loaded from `data/`
- Embeddings are created (requires OpenAI API calls)
- Index is stored in Pinecone
- Local metadata is cached

On subsequent runs, the cached index is loaded (faster startup).

To force re-indexing, delete the `data/vector_store/` directory. 

### Performance Considerations

- **First Query**: May take longer due to Pinecone initialisation
- **Subsequent Queries**: Fast retrieval from vector store
- **Embedding Costs**: Each new document incurs OpenAI API costs
- **Vector Store**: Pinecone has limits on the free tier


## Approach & Design Decisions

This project demonstrates production-ready software engineering practices while maintaining simplicity and focus:

- **Modular Architecture**: Separation of concerns (routes, models, business logic) for maintainability
- **Type Safety**: Pydantic models throughout for runtime validation and better developer experience
- **Cloud-Native Design**: Stateless application with externalised configuration for easy scaling
- **Observability**: Structured logging to stdout for integration with log aggregation systems
- **Security-First**: API keys via environment variables, never hardcoded
- **Documentation-Driven**: Interactive API docs auto-generated from code


## Simplifications

The assignment involves developing a RAG system within the context of a chatbot. The development of the solution followed a simplified approach to focus more on some key points:
- The development of a working RAG system using a Pinecone database
- The development of a FastAPI application, exposing an endpoint to use the RAG system
- The containerisation of the application using Docker containers
- Providing essential files to deploy the application in a Kubernetes environment.

### Simplifications applied:
- The application involves only the RAG system and exposes its endpoint. An external application would implement the chatbot itself using the RAG endpoint for each query.
- To reduce development time, the content of the web pages has been copied and saved in .txt files, stored in the data directory.
- The solution has been developed using some default configurations and models.

In particular:
- Embeddings are computed using "text-embedding-ada-002" from OpenAI.
- GPT-3.5-turbo language model is used.
- Top-k similarity retrieval is used.
- Default prompt and "compact" method are used to consider retrieved chunks to create an answer.

### What a production implementation would additionally include:
- **Streaming chat interface**: Real-time token streaming for better UX
- **Conversation memory**: Session management to maintain context across queries
- **Authentication & Authorization**: User management and API key authentication
- **Rate limiting**: Prevent abuse and manage costs
- **Caching layer**: Redis for frequently asked questions
- **Monitoring & Observability**: Prometheus metrics, distributed tracing
- **Automated testing**: Unit tests, integration tests, and E2E tests
- **CI/CD pipeline**: Automated builds, tests, and deployments


## Possible Future Improvements

There are several possible improvements to experiment with at different stages in the system.

1. **Document Ingestion**: Text files are loaded from `data/` directory. It would be better to access data stored in a different location
2. **Chunking**: Documents are split into manageable chunks, by sentence and depend on the default chunk size (matching the default embedding model). However, two issues can arise: the relevant information might be scattered in too many chunks and/or chunks can also contain non-relevant information that can act as a distractor. An improvement would be achieved using semantic chunking. This consists of grouping together different sentences of the document, based on their embeddings, and then chunking them. This would enhance the quality of retrieval, since the chunking would take into account the meaning and context of the text.
3. **Embedding**: Each chunk is converted to a vector using an off-the-shelf OpenAI embedding model. Using general-purpose models can generate embeddings that are similar in general linguistic context, but they might not be ideal in the specific context and jargon used in some documents. Another possible improvement in a RAG system would be to fine-tune an embedding model for the documents used by the system. This would ensure that nuances related to context and language used would be captured by the embeddings.
4. **Indexing**: Vectors are stored in Pinecone for fast retrieval. The index is given a fixed name, and then data is stored locally to retrieve and rebuild the objects for subsequent runs of the project. To force the rebuild of the vector store, it is necessary to delete the directory where it has been saved. A better and smoother management would include an option to force rebuild by automatically deleting and recreating the vector store, without further manual intervention.
5. **Retrieval**: The system performs a semantic search to retrieve information. A first improvement would be achieved using a hybrid approach, combining semantic search with keyword-based search for better retrieval. Moreover, the specific semantic search can be further improved. User questions are embedded, and the top-k similar vectors are retrieved. This is the simplest retrieval method and has some downsides. First of all, it guarantees to retrieve at least one similar vector, but this also happens when there is no actual relevant information in the chunks stored. On the other hand, the retrieval quality is dependent on the chunking method and the embedding used. Several techniques can be applied to mitigate these issues. One is to use query expansion, which involves using an LLM to generate an expected form of answer and provide it as context as an example (expansion with generated answer) or using an LLM to generate related questions to the original one and retrieve documents for all the queries (expansion with multiple queries). These techniques help mitigate issues related to distractors in chunks (the first) and scattered information (the second). Moreover, similarity in embedding does not necessarily mean actual relevance of a chunk to the query. An improvement in retrieval can be applied by re-ranking the retrieved chunks and selecting the most relevant ones based on the new ranking.
6. **Synthesis**: Retrieved chunks are passed as context and used to generate answers. The default prompt and synthesiser are used for this task. Further improvements can be achieved using a custom prompt and different ways to pass the chunks as context to the language model that generates the answer. Better prompt engineering could also produce answers in a form that is more pleasing to a human reader, and that might better represent the company itself. Moreover, the default language model is used for the answer, hence, an improvement could be achieved using the state of the art.
7. **Nice to have**: The system uses .txt files obtained from the content of help centre web pages. However, the pages considered originally also contain images. It might be useful to have multi-modal support for images and tables.

Considering possible priorities, improvements can be summed up as follows:

### High Priority
1. Hybrid Search
2. Query Expansion & Re-ranking
3. Automated Vector Store Management

### Medium Priority
4. Semantic Chunking
5. Fine-tuned Embeddings
6. Advanced Prompt Engineering

### Low Priority / Nice-to-Have
7. Multi-modal Support



## Use of AI

An AI assistant has been used in the development of this project. Specifically, Claude sonnet 4.5 has been used for the generation of the Helm files for deployment on Kubernetes environments and the relative documentation.



## Author

Sandra La Mantia

---

**Built with ❤️ using FastAPI, LlamaIndex, and Pinecone**


