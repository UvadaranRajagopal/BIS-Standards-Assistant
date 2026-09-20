"""
Ingest BIS standards from JSON into ChromaDB.
Supports the current BIS dataset schema.
"""

import json
import sys
from pathlib import Path

# Allow imports from the backend folder
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag.chroma_db import (
    add_standards_batch,
    get_collection_stats,
    clear_collection,
)


def ingest_standards(
    json_path: str = "data/standards_metadata.json"
):
    """Load BIS standards from JSON and add them to ChromaDB."""

    print("=" * 60)
    print("BIS STANDARDS INGESTION")
    print("=" * 60)

    # ---------------------------------------------------------
    # Load JSON
    # ---------------------------------------------------------
    print(f"\nLoading standards from {json_path}...")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {json_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False

    # ---------------------------------------------------------
    # Support both:
    #
    # 1. New format:
    # [
    #   {...},
    #   {...}
    # ]
    #
    # 2. Old format:
    # {
    #   "standards": [
    #       {...}
    #   ]
    # }
    # ---------------------------------------------------------
    if isinstance(data, list):
        standards = data
    elif isinstance(data, dict):
        standards = data.get("standards", [])
    else:
        print("❌ Unsupported JSON structure")
        return False

    print(f"Found {len(standards)} standards")

    if not standards:
        print("❌ No standards found in JSON file")
        return False

    # ---------------------------------------------------------
    # Prepare documents
    # ---------------------------------------------------------
    documents = []

    for index, std in enumerate(standards, start=1):

        is_number = std.get("is_number", "")
        title = std.get("title", "")
        year = std.get("year")
        status = std.get("status")
        scope = std.get("scope")

        certification = std.get("certification", {})
        relationships = std.get("relationships", {})
        bis_source = std.get("bis_source", {})

        # -----------------------------------------------------
        # Certification information
        # -----------------------------------------------------
        certification_applicable = certification.get(
            "applicable"
        )

        certification_details = certification.get(
            "details"
        )

        qco = certification.get("qco")
        crs = certification.get("crs")

        # -----------------------------------------------------
        # BIS relationships
        # -----------------------------------------------------
        referred_indian_standards = relationships.get(
            "referred_indian_standards", []
        )

        referred_in_following_standards = relationships.get(
            "referred_in_following_standards", []
        )

        # Make sure these are lists
        if not isinstance(referred_indian_standards, list):
            referred_indian_standards = []

        if not isinstance(referred_in_following_standards, list):
            referred_in_following_standards = []

        # -----------------------------------------------------
        # BIS source
        # -----------------------------------------------------
        official_bis_url = bis_source.get(
            "official_url"
        )

        # -----------------------------------------------------
        # Build searchable text
        #
        # This is what gets embedded by the RAG system.
        # -----------------------------------------------------
        searchable_parts = [
            is_number,
            title,
        ]

        if year is not None:
            searchable_parts.append(
                f"Year: {year}"
            )

        if status:
            searchable_parts.append(
                f"Status: {status}"
            )

        if scope:
            searchable_parts.append(
                f"Scope: {scope}"
            )

        if certification_details:
            searchable_parts.append(
                f"Certification: {certification_details}"
            )

        if certification_applicable is not None:
            searchable_parts.append(
                f"Certification applicable: "
                f"{certification_applicable}"
            )

        if qco is not None:
            searchable_parts.append(
                f"QCO applicable: {qco}"
            )

        if crs is not None:
            searchable_parts.append(
                f"CRS applicable: {crs}"
            )

        if referred_indian_standards:
            searchable_parts.append(
                "Referred Indian Standards: "
                + ", ".join(referred_indian_standards)
            )

        if referred_in_following_standards:
            searchable_parts.append(
                "Referred in following Indian Standards: "
                + ", ".join(
                    referred_in_following_standards
                )
            )

        searchable_text = "\n".join(
            str(part)
            for part in searchable_parts
            if part
        ).strip()

        # -----------------------------------------------------
        # Create unique Chroma document ID
        #
        # The new BIS dataset doesn't contain an "id" field,
        # so we generate a stable ID from the IS number.
        # -----------------------------------------------------
        document_id = (
            is_number
            .replace(" ", "_")
            .replace("/", "_")
            .replace(":", "_")
        )

        if not document_id:
            document_id = f"standard_{index}"

        # -----------------------------------------------------
        # Metadata stored alongside the embedding
        # -----------------------------------------------------
        metadata = {
            "is_number": is_number,
            "title": title,
            "year": year if year is not None else 0,
            "status": status if status else "Unknown",
            "scope": scope if scope else "",
            "certification_applicable": (
                str(certification_applicable)
                if certification_applicable is not None
                else ""
            ),
            "certification_details": (
                certification_details
                if certification_details
                else ""
            ),
            "qco": (
                str(qco)
                if qco is not None
                else ""
            ),
            "crs": (
                str(crs)
                if crs is not None
                else ""
            ),
            "bis_url": (
                official_bis_url
                if official_bis_url
                else ""
            ),
            "referred_indian_standards": (
                ", ".join(referred_indian_standards)
            ),
            "referred_in_following_standards": (
                ", ".join(
                    referred_in_following_standards
                )
            ),
        }

        documents.append({
            "id": document_id,
            "text": searchable_text,
            "metadata": metadata,
        })

    # ---------------------------------------------------------
    # Show what is going to be ingested
    # ---------------------------------------------------------
    print("\nPreparing documents...")

    for document in documents:
        print(
            f"  ✓ {document['metadata']['is_number']} - "
            f"{document['metadata']['title']}"
        )

    # ---------------------------------------------------------
    # Clear existing ChromaDB collection
    # ---------------------------------------------------------
    print("\nClearing existing collection...")
    clear_collection()

    # ---------------------------------------------------------
    # Add new documents
    # ---------------------------------------------------------
    print("\nAdding standards to ChromaDB...")

    try:
        add_standards_batch(documents)
    except Exception as e:
        print(
            f"\n❌ Failed to add standards to ChromaDB: {e}"
        )
        return False

    # ---------------------------------------------------------
    # Database statistics
    # ---------------------------------------------------------
    stats = get_collection_stats()

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)

    print(
        f"Total standards in database: "
        f"{stats['total_documents']}"
    )

    print(
        f"Collection: "
        f"{stats['collection_name']}"
    )

    print(
        f"Embedding model: "
        f"{stats['embedding_model']}"
    )

    print("=" * 60)

    return True


if __name__ == "__main__":
    success = ingest_standards()
    raise SystemExit(0 if success else 1)