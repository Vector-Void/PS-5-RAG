# RAG Assistant

A Retrieval-Augmented Generation (RAG) system for document-based question answering. Upload documents and ask questions to receive answers grounded in their content.

## Features

* Document ingestion and text extraction
* Text chunking for efficient retrieval
* Semantic embeddings using Sentence Transformers
* Vector storage and similarity search using ChromaDB
* Context-grounded answers generated using Groq
* FastAPI backend
* Streamlit frontend

## Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Embeddings:** Sentence Transformers
* **Vector Database:** ChromaDB
* **LLM:** Groq API
* **Language:** Python

## Project Structure

```text
PS-5-RAG/
├── rag_backend/
│   ├── app.py
│   ├── requirements.txt
│   └── src/
│       ├── data_loader.py
│       ├── embedding.py
│       ├── search.py
│       └── vectorstore.py
├── rag_frontend/
│   └── streamlit_app.py
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vector-Void/PS-5-RAG.git
cd PS-5-RAG
```

### 2. Install backend dependencies

```bash
cd rag_backend
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside `rag_backend` and add your Groq API key using the variable name expected by the application.

**Never commit your API key or `.env` file to GitHub.**

### 4. Start the backend

From the `rag_backend` directory:

```bash
python -m uvicorn app:app --reload
```

Backend API documentation:

http://127.0.0.1:8000/docs

### 5. Start the frontend

Open another terminal, activate the appropriate Python environment, and run:

```bash
cd rag_frontend
streamlit run streamlit_app.py
```

## How It Works

1. Documents are processed and divided into chunks.
2. Text chunks are converted into vector embeddings.
3. Embeddings are stored in ChromaDB.
4. A user's question retrieves relevant document content.
5. The retrieved context is passed to the language model to generate an answer.

## Future Improvements

* Support for additional document formats
* Improved retrieval and reranking
* Source citations in generated answers
* Deployment for public access
* Automated testing
