from app.rag.chroma_db import collection


def check_version(standard_id: str) -> dict:
    """
    Check revision information for a BIS standard
    using the metadata stored in the knowledge base.
    """

    result = collection.get(
        ids=[standard_id],
        include=["metadatas"]
    )

    if not result["ids"]:
        return {
            "standard_id": standard_id,
            "status": "NOT_FOUND",
            "message": "Standard not found in knowledge base."
        }

    metadata = result["metadatas"][0]

    latest_version = metadata.get("latest_version")
    year = metadata.get("year")
    status = metadata.get("status", "Verify")

    if latest_version:

        if str(latest_version) != str(year):
            return {
                "standard_id": standard_id,
                "current_version": latest_version,
                "dataset_version": year,
                "status": "NEWER_REVISION_AVAILABLE",
                "message": (
                    f"A newer revision ({latest_version}) "
                    f"is available compared with the dataset version ({year})."
                )
            }

        return {
            "standard_id": standard_id,
            "current_version": latest_version,
            "dataset_version": year,
            "status": "CURRENT",
            "message": (
                "No newer revision is recorded in the knowledge base."
            )
        }

    return {
        "standard_id": standard_id,
        "current_version": year,
        "dataset_version": year,
        "status": "VERIFY",
        "message": (
            "Revision information should be verified "
            "against the latest official BIS record."
        )
    }


def check_versions(standard_ids: list[str]) -> list[dict]:
    """
    Check version information for multiple BIS standards.
    """

    return [
        check_version(standard_id)
        for standard_id in standard_ids
    ]