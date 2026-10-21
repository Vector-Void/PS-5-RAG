from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Convert text into numerical vectors."""
    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


def generate_query_embedding(query: str) -> list[float]:
    """Convert a user's question into a numerical vector."""
    return generate_embeddings([query])[0]