from fastapi import APIRouter, Query
from pathlib import Path
import json

router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)


@router.get("/standards")
async def get_standards_graph(
    standards: list[str] = Query(default=[])
):
    """
    Return a focused relationship graph for the requested standards.

    If no standards are provided, all standards are returned.
    """

    metadata_path = (
        Path(__file__).resolve().parents[3]
        / "data"
        / "standards_metadata.json"
    )

    with open(metadata_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    all_standards = data["standards"]

    # ---------------------------------------------------------
    # If specific standards were provided, use only those
    # plus their directly related standards.
    # ---------------------------------------------------------

    if standards:

        selected_numbers = set(standards)

        # Find the selected standards
        selected_standards = [
            standard
            for standard in all_standards
            if standard["is_number"] in selected_numbers
        ]

        # Add their direct relationships
        related_numbers = set()

        for standard in selected_standards:
            for related in standard.get("related_standards", []):
                related_numbers.add(related)

        # Add related standards that actually exist
        focused_numbers = selected_numbers.union(related_numbers)

        standards_to_show = [
            standard
            for standard in all_standards
            if standard["is_number"] in focused_numbers
        ]

    else:

        # No filter → return everything
        standards_to_show = all_standards


    # ---------------------------------------------------------
    # Create graph nodes
    # ---------------------------------------------------------

    nodes = []

    for standard in standards_to_show:

        nodes.append({
            "id": standard["is_number"],
            "label": standard["is_number"],
            "title": standard["title"],
            "category": standard["category"]
        })


    # ---------------------------------------------------------
    # Create relationships
    # ---------------------------------------------------------

    standard_numbers = {
        standard["is_number"]
        for standard in standards_to_show
    }

    edges = []

    for standard in standards_to_show:

        source = standard["is_number"]

        for related in standard.get("related_standards", []):

            # Only connect standards that are
            # actually visible in this graph.
            if related in standard_numbers:

                edges.append({
                    "source": source,
                    "target": related,
                    "relationship": "RELATED"
                })


    return {
        "nodes": nodes,
        "edges": edges
    }