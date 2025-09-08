# AdvancedRAG: LangChain Documentation Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Cohere, and Streamlit for querying LangChain documentation. This project demonstrates LLMOps practices with containerization, monitoring, and scalable deployment.

## Features

- **RAG Pipeline**: Retrieves and reranks relevant documents using Cohere's reranking API.
- **LangChain Integration**: Leverages LangChain for LLM interactions and document processing.
- **Langgraph Intergration**: Leverages Langgraph to build a flow of the application. 
- **Streamlit Frontend**: User-friendly chat interface with message history.
- **Monitoring**: Integrated with LangFuse for tracing and analytics.
- **Containerized**: Docker support for easy deployment.

## Project Structure

```
AdvancedRAG/
├── .env                    # Environment variables
├── .git/                   # Git repository
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker configuration
├── README.md               # This file
├── app.py                  # Streamlit chatbot interface
├── data/
│   ├── raw/                # Raw LangChain documentation (.mdx files)
│   └── vectorstore/        # Vectorstore data
├── logs.txt                # Application logs
├── requirements.txt        # Python dependencies
└── src/
    ├── core/
    │   ├── tracing.py      # Tracing utilities
    │   └── utils.py        # Core utilities
    ├── db/
    │   └── chroma_db.py    # Chroma database interactions
    ├── main.py             # Main application logic and ask_question function
    ├── rag/
    │   ├── __init__.py
    │   ├── config.py       # RAG configuration
    │   ├── generator.py    # Response generation
    │   ├── graph.py        # LangGraph workflow for RAG
    │   ├── nodes.py        # Graph nodes
    │   ├── pipeline.py     # Pipeline orchestration
    │   ├── prompt.py       # Chat prompts
    │   └── state.py        # State management
    ├── scripts/
    │   ├── ingest_data.py  # Data ingestion script
    │   └── retrieve_data.py # Data retrieval utilities
    └── utils/
        ├── __init__.py
        └── logger.py       # Logging utilities
```

## Prerequisites

- Python 3.12+
- Docker (for containerization)
- API keys for Cohere, LangFuse and GitHub

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/AdvancedRAG.git
   cd AdvancedRAG
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

1. **Run the Streamlit app**:
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
