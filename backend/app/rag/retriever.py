"""
Semantic search retriever for BIS standards.
"""

from app.rag.chroma_db import (
    search_standards,
    get_collection_stats,
    collection
)


def retrieve_standards(
    query: str,
    top_k: int = None
) -> list[dict]:
    """
    Retrieve relevant BIS standards for a procurement query.
    """

    results = search_standards(query, top_k)

    # Highest relevance first
    results.sort(
        key=lambda x: x["relevance_score"],
        reverse=True
    )

    return results


def test_retrieval():
    """Test semantic retrieval."""

    print("=" * 60)
    print("RETRIEVAL TEST")
    print("=" * 60)

    test_queries = [
        "LED street lights for highway",
        "Office chairs for conference room",
        "Electrical cables for building wiring",
        "Laptop computers for office use"
    ]

    stats = get_collection_stats()

    print(
        f"\nDatabase has "
        f"{stats['total_documents']} standards\n"
    )

    for query in test_queries:

        print(f"Query: '{query}'")

        results = retrieve_standards(
            query,
            top_k=2
        )

        for result in results:

            metadata = result["metadata"]

            print(
                f"  ✓ {metadata['is_number']} "
                f"- {metadata['title']}"
            )

            print(
                f"    Relevance: "
                f"{result['relevance_score']}%"
            )

            print(
                f"    Category: "
                f"{metadata['category']}"
            )

        print()

    print("=" * 60)


if __name__ == "__main__":
    test_retrieval()

from app.rag.chroma_db import collection

def get_related_standards(standard_id: str) -> list[dict]:
    result = collection.get(
        ids=[standard_id],
        include=["documents", "metadatas"]
    )

    if not result["ids"]:
        return []

    related = collection.query(
        query_texts=[result["documents"][0]],
        n_results=4,
        include=["documents", "metadatas", "distances"]
    )

    formatted = []

    for i, related_id in enumerate(related["ids"][0]):
        if related_id == standard_id:
            continue

        formatted.append({
            "id": related_id,
            "document": related["documents"][0][i],
            "metadata": related["metadatas"][0][i],
            "distance": related["distances"][0][i]
        })

    return formatted[:3]