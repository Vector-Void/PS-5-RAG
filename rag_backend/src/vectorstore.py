import chromadb
from pathlib import Path

from src.embedding import generate_embeddings


DB_PATH = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "documents"

_client = chromadb.PersistentClient(path=str(DB_PATH))

_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)


def add_documents(chunks: list[dict]) -> int:
    """Store document chunks and their embeddings in ChromaDB."""
    if not chunks:
        return 0

    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "filename": chunk["filename"],
            "page": chunk["page"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    _collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)


def search_documents(query: str, top_k: int = 5) -> list[dict]:
    """Retrieve the most relevant document chunks for a question."""
    if not query.strip():
        return []

    if _collection.count() == 0:
        return []

    query_embedding = generate_embeddings([query])[0]

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, _collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for i, text in enumerate(results["documents"][0]):
        matches.append({
            "text": text,
            "filename": results["metadatas"][0][i]["filename"],
            "page": results["metadatas"][0][i]["page"],
            "distance": results["distances"][0][i],
        })

    return matches