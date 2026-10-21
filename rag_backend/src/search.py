import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.vectorstore import search_documents


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def generate_answer(question: str, top_k: int = 5) -> dict:
    """Answer questions using retrieved document context."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    load_dotenv(ENV_PATH, override=True)

    sources = search_documents(question, top_k=top_k)

    if not sources:
        return {
            "answer": "I couldn't find relevant information in the uploaded documents.",
            "sources": [],
        }

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_actual_api_key_here":
        raise RuntimeError(
            "Groq API key is missing. Add your actual key to the project's .env file."
        )

    model_name = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    )

    context = "\n\n".join(
        f"[Source: {source['filename']}, Page: {source['page']}]\n"
        f"{source['text']}"
        for source in sources
    )

    llm = ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0,
    )

    response = llm.invoke([
        SystemMessage(
            content=(
                "Answer using only the provided document context. "
                "If the answer is not present, say so. "
                "Do not invent facts or citations. "
                "Cite supporting filenames and page numbers."
            )
        ),
        HumanMessage(
            content=f"DOCUMENT CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        ),
    ])

    return {
        "answer": response.content,
        "sources": [
            {
                "filename": source["filename"],
                "page": source["page"],
                "distance": source["distance"],
            }
            for source in sources
        ],
    }