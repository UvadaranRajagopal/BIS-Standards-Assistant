"""
ChromaDB vector database for storing and searching BIS standards.
Uses persistent storage so data survives server restarts.
"""

import chromadb
from app.config import settings
from app.rag.embeddings import get_embeddings


# Initialize persistent ChromaDB client
client = chromadb.PersistentClient(
    path=settings.CHROMA_PERSIST_DIR
)


# Get or create collection
collection = client.get_or_create_collection(
    name="bis_standards",
    metadata={
        "description": "BIS standards for procurement",
        "embedding_model": settings.EMBEDDING_MODEL
    }
)


def add_standard(
    standard_id: str,
    text: str,
    metadata: dict
):
    """Add a single standard to ChromaDB."""

    embedding = get_embeddings([text])[0]

    collection.add(
        ids=[standard_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )

    print(f"✓ Added {standard_id} to ChromaDB")


def add_standards_batch(standards: list[dict]):
    """Add multiple standards to ChromaDB."""

    ids = [s["id"] for s in standards]
    texts = [s["text"] for s in standards]
    metadatas = [s["metadata"] for s in standards]

    print(
        f"Generating embeddings for "
        f"{len(standards)} standards..."
    )

    embeddings = get_embeddings(texts)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

    print(
        f"✓ Added {len(standards)} standards to ChromaDB"
    )


def search_standards(query: str, top_k: int = None) -> list:
    if top_k is None:
        top_k = settings.TOP_K_RESULTS

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    formatted_results = []

    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]

        # ChromaDB is using squared L2 distance.
        # Our embeddings are normalized, so:
        # cosine_similarity = 1 - (distance / 2)
        similarity = 1 - (distance / 2)

        relevance_score = round(
            max(0, min(100, similarity * 100)),
            2
        )

        formatted_results.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": distance,
            "relevance_score": relevance_score
        })

    return formatted_results


def get_collection_stats() -> dict:
    """Get statistics about the collection."""

    return {
        "total_documents": collection.count(),
        "collection_name": collection.name,
        "embedding_model": settings.EMBEDDING_MODEL
    }


def clear_collection():
    """Delete all documents from the collection."""

    ids = collection.get()["ids"]

    if ids:
        collection.delete(ids=ids)

    print("✓ Cleared ChromaDB collection")


print(
    f"ChromaDB initialized: "
    f"{get_collection_stats()}"
)

