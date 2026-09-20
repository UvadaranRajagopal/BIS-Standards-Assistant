import json

def validate_standards_data(json_path: str = "data/standards_metadata.json"):
    """Validate BIS standards dataset for completeness and correctness."""

    print("=" * 60)
    print("BIS STANDARDS DATA VALIDATION")
    print("=" * 60)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n✓ Metadata present: {bool(data.get('metadata'))}")

    standards = data.get("standards", [])
    print(f"✓ Total standards: {len(standards)}")

    categories = set()
    for std in standards:
        categories.add(std.get("category", "Unknown"))

    print(f"✓ Categories covered: {len(categories)} - {categories}")

    print("\nValidating each standard:")

    required_fields = [
        "id",
        "is_number",
        "title",
        "scope",
        "year",
        "status"
    ]

    all_valid = True

    for i, std in enumerate(standards, 1):
        missing = [
            field for field in required_fields
            if field not in std
        ]

        if missing:
            print(
                f"  ❌ Standard {i} "
                f"({std.get('is_number', 'UNKNOWN')}): "
                f"Missing {missing}"
            )
            all_valid = False
        else:
            print(
                f"  ✓ Standard {i} "
                f"({std['is_number']}): OK"
            )

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    print(f"Total standards: {len(standards)}")
    print(f"Categories: {len(categories)}")
    print("Target: 20+ standards across 3+ categories")

    if len(standards) >= 20 and len(categories) >= 3 and all_valid:
        print("\n✅ DATASET READY FOR EMBEDDINGS")
        return True

    print("\n⚠️ DATASET NEEDS ATTENTION")
    return False


if __name__ == "__main__":
    is_ready = validate_standards_data()
    raise SystemExit(0 if is_ready else 1)