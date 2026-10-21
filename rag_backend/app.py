import uuid
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from src.data_loader import extract_text_from_pdf
from src.vectorstore import add_documents
from src.search import generate_answer


app = FastAPI(
    title="RAG Document Assistant",
    description="Upload PDFs and ask questions using AI.",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=10)


def chunk_pages(
    pages: list[dict],
    filename: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """Split extracted page text into overlapping chunks."""

    chunks = []

    for page in pages:
        text = page["text"]
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": chunk_text,
                    "filename": filename,
                    "page": page["page"],
                    "chunk_index": chunk_index,
                })

                chunk_index += 1

            if end == len(text):
                break

            start = end - overlap

    return chunks


@app.get("/")
def home():
    return {
        "message": "RAG Document Assistant is running!",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, extract its text, chunk it, and index it."""

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    document_id = str(uuid.uuid4())
    original_filename = Path(file.filename).name
    stored_filename = f"{document_id}.pdf"
    file_path = DATA_DIR / stored_filename

    try:
        total_size = 0
        max_size = 20 * 1024 * 1024  # 20 MB

        with file_path.open("wb") as destination:
            while True:
                content = await file.read(1024 * 1024)

                if not content:
                    break

                total_size += len(content)

                if total_size > max_size:
                    raise HTTPException(
                        status_code=413,
                        detail="PDF exceeds the 20 MB upload limit.",
                    )

                destination.write(content)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty.",
            )

        try:
            pages = extract_text_from_pdf(str(file_path))
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        chunks = chunk_pages(pages, original_filename)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No usable text could be extracted from the PDF.",
            )

        indexed_count = add_documents(chunks)

        return {
            "message": "Document uploaded and indexed successfully.",
            "document_id": document_id,
            "filename": original_filename,
            "pages_extracted": len(pages),
            "chunks_indexed": indexed_count,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(exc)}",
        )

    finally:
        await file.close()

        if file_path.exists():
            file_path.unlink()


@app.post("/query")
def query_documents(request: QueryRequest):
    """Answer a question using the indexed documents."""

    try:
        return generate_answer(
            question=request.question.strip(),
            top_k=request.top_k,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the question. Check the backend logs.",
        )