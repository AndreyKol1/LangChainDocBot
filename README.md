# LangChain Documentation Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Cohere, and Streamlit for querying LangChain documentation. This project demonstrates LLMOps practices with containerization, monitoring, and scalable deployment.

## Features

- **RAG Pipeline**: Retrieves and reranks relevant documents using Cohere's reranking API. Utilizes **Query Transformation** and
**Contextual Compression** for better retrieval process.
- **LangChain Integration**: Leverages LangChain for LLM interactions and document processing.
- **Langgraph Intergration**: Leverages Langgraph to build a flow of the application. 
- **Streamlit Frontend**: User-friendly chat interface with message history.
- **Monitoring**: Integrated with LangFuse for tracing and analytics.
- **Containerized**: Docker support for easy deployment.

## Project Structure

```
AdvancedRAG/
├── .dockerignore          # Docker ignore file
├── .env                   # Environment variables
├── .git/                  # Git repository
├── .gitignore             # Git ignore file
├── Dockerfile             # Docker configuration
├── README.md              # This file
├── app.py                 # Streamlit chatbot interface
├── model/                 # Cached all-MiniLM-L6-v2 embedding model files
├── requirements.txt       # Python dependencies
├── src/
│   ├── core/
│   │   ├── tracing.py     # Tracing utilities
│   │   └── utils.py       # Core utilities
│   ├── db/
│   │   └── chroma_db.py   # Chroma database interactions
│   ├── main.py            # Main application logic and ask_question function
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── config.py      # RAG configuration
│   │   ├── generator.py   # Response generation
│   │   ├── graph.py       # LangGraph workflow for RAG
│   │   ├── nodes.py       # Graph nodes
│   │   ├── pipeline.py    # Pipeline orchestration
│   │   ├── prompt.py      # Chat prompts
│   │   └── state.py       # State management
│   ├── scripts/
│   │   ├── datapipeline.py # Data pipeline script
│   │   ├── ingest_data.py # Data ingestion utilities
│   │   └── retrieve_data.py # Data retrieval utilities
│   └── utils/
│       ├── __init__.py
│       ├── gcp.py         # GCP utilities
│       └── logger.py      # Logging utilities
```

## Prerequisites

- Python 3.12+
- Docker (for containerization)
- API keys for Cohere, LangFuse and GitHub

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/LangChainDocBot.git
   cd LangChainDocBot
   ```

2. **Set up environment**:
   ```bash
   conda create -n advancedrag python=3.12
   conda activate advancedrag
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```
   COHERE_API=your_cohere_api_key
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   GITHUB_TOKEN=your_github_token
   ```

## Usage

### Local Development

1. **Fetrch, process and ingest data**:
    ```bash
    python3 src/scripts/datapipeline.py
    ```
    
2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```
   Access at `http://localhost:8501`

### Docker

1. **Build the image**:
   ```bash
   docker build -t advancedrag .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8501:8501 advancedrag
   ```

## Deployment

### Google Cloud Platform (GCP)

1. **Build and push to Google Container Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/advancedrag
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy langchainbot \
     --image gcr.io/YOUR_PROJECT_ID/advancedrag \
     --platform managed \
     --region europe-west1 \
     --allow-unauthenticated \
     --memory 2Gi \
     --set-env-vars COHERE_API=YOUR_COHERE_KEY,LANGFUSE_PUBLIC_KEY=YOUR_PUBLIC_KEY,LANGFUSE_SECRET_KEY=YOUR_SECRET_KEY,GROQ_API_KEY=YOUR_GROQ_KEY,BUCKET_NAME=YOUR_BUCKET,GCS_PERSIST_PATH=chroma/,LOCAL_PERSIST_PATH=./vectorstore
   ```

### Environment Variables

Required environment variables for deployment:
- `COHERE_API`: Cohere API key
- `LANGFUSE_PUBLIC_KEY`: LangFuse public key
- `LANGFUSE_SECRET_KEY`: LangFuse secret key
- `GROQ_API_KEY`: Groq API key
- `BUCKET_NAME`: GCP bucket name for vectorstore
- `GCS_PERSIST_PATH`: Path in GCS bucket (default: chroma/)
- `LOCAL_PERSIST_PATH`: Local path for vectorstore (default: /tmp/vectorstore)
