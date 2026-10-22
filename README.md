# RAG Assistant

A Retrieval-Augmented Generation (RAG) system that lets you upload PDF documents and ask questions about their content. It retrieves relevant information from your documents and uses a Large Language Model (LLM) to generate answers grounded in the retrieved content.

## Features

* PDF text extraction using PyMuPDF
* Text chunking for efficient retrieval
* Semantic embeddings using Sentence Transformers
* Vector storage and similarity search using ChromaDB
* Context-grounded answer generation using the Groq API
* FastAPI backend with interactive API documentation
* Streamlit frontend for interacting with the system
* Persistent storage of indexed document embeddings

## Tech Stack

| Component       | Technology            |
| --------------- | --------------------- |
| Language        | Python                |
| Backend         | FastAPI               |
| Frontend        | Streamlit             |
| Embeddings      | Sentence Transformers |
| Vector Database | ChromaDB              |
| LLM Provider    | Groq API              |
| PDF Processing  | PyMuPDF               |

## Project Structure

```text
PS-5-RAG/
├── rag_backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   └── src/
│       ├── data_loader.py
│       ├── embedding.py
│       ├── search.py
│       └── vectorstore.py
├── rag_frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

Before getting started, install:

* Python 3.13 or a compatible Python version
* Git
* A Groq API key

Get your API key from the [Groq Console](https://console.groq.com/).

## Installation and Setup

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/Vector-Void/PS-5-RAG.git
cd PS-5-RAG
```

### 2. Set Up the Backend

From the project root, run:

```powershell
cd rag_backend
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

**If PowerShell blocks environment activation**, you can use the virtual environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure Environment Variables

Make sure you are inside the `rag_backend` directory.

Create your local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Open `rag_backend/.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Replace `your_groq_api_key_here` with your actual API key.

The model shown above is an example configuration. You can change `GROQ_MODEL` to another model supported by your Groq account.

**Security:** Never share your API key or commit your `.env` file to GitHub. The repository includes `.env.example` so users can configure their own credentials.

### 4. Start the Backend

Make sure you are in the `rag_backend` directory and that your backend virtual environment is active.

Run:

```powershell
python -m uvicorn app:app --reload
```

The backend should now be available at:

* **API:** http://127.0.0.1:8000
* **Interactive API documentation:** http://127.0.0.1:8000/docs

Keep this terminal open while using the application.

### 5. Set Up the Frontend

Open a **second terminal** in the project root.

Navigate to the frontend directory:

```powershell
cd rag_frontend
```

Create a separate virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the frontend dependencies:

```powershell
python -m pip install -r requirements.txt
```

If activation is blocked, install the dependencies directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 6. Launch the Frontend

From the `rag_frontend` directory, run:

```powershell
streamlit run streamlit_app.py
```

Streamlit will display a local URL, typically:

http://localhost:8501

Open this URL in your browser to use the application.

**Important:** The frontend is configured to communicate with the backend at `http://127.0.0.1:8000`. Keep both terminals running while using the application.

## How It Works

1. **Document ingestion:** PDF documents are uploaded and their text is extracted.
2. **Chunking:** The extracted text is divided into smaller chunks.
3. **Embedding generation:** Sentence Transformers converts text chunks into numerical vector embeddings.
4. **Vector storage:** The embeddings and associated document content are stored in ChromaDB.
5. **Semantic retrieval:** When a user asks a question, the system retrieves relevant document content.
6. **Answer generation:** The retrieved context is passed to the configured Groq model to generate a response grounded in the available information.

## Configuration

The backend uses the following environment variables:

| Variable       | Description                                          |
| -------------- | ---------------------------------------------------- |
| `GROQ_API_KEY` | Your Groq API key                                    |
| `GROQ_MODEL`   | The Groq model identifier used for answer generation |

If `GROQ_MODEL` is not specified, the application uses its internal default model, `llama-3.3-70b-versatile`, provided that model remains available to your Groq account.

## Data and Storage

* Indexed document embeddings are persisted in `rag_backend/chroma_db`.
* Uploaded PDF files may be stored temporarily during processing.
* Local vector database files, uploaded documents, and environment files are excluded from version control.

The vector database is generated locally as you use the application; it does not need to be committed to GitHub.

## Troubleshooting

### Backend fails to start

* Make sure you are inside the `rag_backend` directory.
* Verify that the backend virtual environment is active.
* Install the dependencies listed in `rag_backend/requirements.txt`.
* Check the terminal output for the specific error.

### Frontend cannot connect to the backend

* Ensure the backend is running at `http://127.0.0.1:8000`.
* Confirm that the frontend's configured API URL matches the backend address.
* Check that both terminals remain open.

### Groq API errors

* Verify that your API key is valid.
* Check that `GROQ_MODEL` specifies a model supported by your Groq account.
* Confirm that your account has the necessary API access and available quota.

### Missing Python packages

Activate the appropriate virtual environment and run:

```powershell
python -m pip install -r requirements.txt
```

Run this command from `rag_backend` for backend dependencies or `rag_frontend` for frontend dependencies.

## Future Improvements

* Support for additional document formats
* Improved retrieval and reranking
* Source citations in generated answers
* Automated testing
* Configurable backend URL
* Deployment options

## Contributing

Contributions, suggestions, and bug reports are welcome. Feel free to open an issue or submit a pull request.

## License

No license has been specified for this repository yet. Until a license is added, others should not assume that they have permission to redistribute or reuse this project's code.
