"""
Embedding generation using sentence-transformers.
Converts text into vectors that capture semantic meaning.
"""

from sentence_transformers import SentenceTransformer
from app.config import settings


# Load the embedding model
# all-MiniLM-L6-v2 creates 384-dimensional embeddings
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)


def get_embedding(text: str) -> list:
    """
    Generate an embedding for a single text.
    """
    embedding = embedding_model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.tolist()


def get_embeddings(texts: list[str]) -> list[list]:
    """
    Generate embeddings for multiple texts.
    """

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()


# Test the embedding system
if __name__ == "__main__":

    test_texts = [
        "LED street lights for highways",
        "Office work chairs",
        "Electrical cables for buildings"
    ]

    print("Generating embeddings for test texts...")

    embeddings = get_embeddings(test_texts)

    print(f"\nGenerated {len(embeddings)} embeddings")
    print(f"Each embedding has {len(embeddings[0])} dimensions")

    print(
        f"First 5 values of first embedding: "
        f"{embeddings[0][:5]}"
    )