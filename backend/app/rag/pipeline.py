"""
Complete RAG pipeline.

Flow:
User query
    ↓
Semantic retrieval from ChromaDB
    ↓
Individual relevance filtering
    ↓
Relevant BIS standards
    ↓
LLM explanation using only relevant retrieved evidence
"""

from app.rag.retriever import retrieve_standards
from app.rag.llm import generate_explanation


# Minimum relevance score required for an individual
# standard to appear as a recommendation.
RELEVANCE_THRESHOLD = 30.0


def analyze_query(
    query: str,
    top_k: int = 3
) -> dict:
    """
    Analyze a procurement query using RAG.

    Every retrieved standard is individually checked against
    the relevance threshold.

    Standards below the threshold are removed completely
    and are not shown as recommendations or passed to the LLM.
    """

    # Step 1: Retrieve candidate BIS standards
    retrieved_standards = retrieve_standards(
        query=query,
        top_k=top_k
    )

    # Step 2: Handle no retrieval results
    if not retrieved_standards:
        return {
            "query": query,
            "standards": [],
            "explanation": (
                "Insufficient relevant BIS information was found "
                "for this procurement requirement."
            )
        }

    # Step 3: Filter EVERY standard individually
    relevant_standards = [
        standard
        for standard in retrieved_standards
        if standard["relevance_score"] >= RELEVANCE_THRESHOLD
    ]

    # Step 4: If no individual result passes the threshold,
    # do not recommend anything.
    if not relevant_standards:

        best_score = retrieved_standards[0]["relevance_score"]

        return {
            "query": query,
            "standards": [],
            "explanation": (
                "Insufficient relevant BIS information was found "
                "for this procurement requirement. "
                f"The highest retrieval relevance was {best_score}%, "
                f"which is below the required threshold of "
                f"{RELEVANCE_THRESHOLD}%."
            )
        }

    # Step 5: Generate explanation ONLY from standards
    # that passed the relevance threshold.
    explanation = generate_explanation(
        query=query,
        retrieved_standards=relevant_standards
    )

    # Step 6: Return only standards that passed the threshold.
    return {
        "query": query,
        "standards": relevant_standards,
        "explanation": explanation
    }


def test_pipeline():
    """Test the complete RAG pipeline."""

    print("=" * 60)
    print("COMPLETE RAG PIPELINE TEST")
    print("=" * 60)

    query = "What standards apply to LED street lights for highways?"

    print(f"\nQuery: {query}")
    print("\nSearching BIS standards and generating explanation...\n")

    result = analyze_query(
        query=query,
        top_k=3
    )

    print("RETRIEVED STANDARDS:")
    print("-" * 60)

    if result["standards"]:

        for i, standard in enumerate(
            result["standards"],
            start=1
        ):

            metadata = standard["metadata"]

            print(
                f"{i}. {metadata['is_number']} - "
                f"{metadata['title']}"
            )

            print(
                f"   Relevance: "
                f"{standard['relevance_score']}%"
            )

    else:

        print(
            "No sufficiently relevant BIS standards found."
        )

    print("\nAI EXPLANATION:")
    print("-" * 60)

    print(result["explanation"])

    print("\n" + "=" * 60)
    print("RAG PIPELINE TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_pipeline()