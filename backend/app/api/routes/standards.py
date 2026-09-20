from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime

from app.audit.audit_chain import audit_logger

from app.config import settings
from app.rag.pipeline import analyze_query
from app.rag.version_checker import check_versions
from app.rag.chroma_db import collection
from app.rag.retriever import get_related_standards
from app.models.schemas import AcceptanceRequest, AcceptanceResponse
from app.pdf.bundle_generator import generate_standards_bundle


router = APIRouter(
    prefix="/standards",
    tags=["Standards"]
)


class AnalyzeRequest(BaseModel):
    query: str
    top_k: int = 3


def build_certification_verification(metadata: dict) -> dict:
    """
    Automatically determine certification requirements
    from verified BIS metadata stored with the standard.
    """

    applicable = metadata.get("certification_applicable")
    details = metadata.get("certification_details")
    qco = metadata.get("qco")
    crs = metadata.get("crs")
    bis_url = metadata.get("bis_url")

    # Convert metadata strings back to booleans safely
    if isinstance(applicable, str):
        applicable_lower = applicable.strip().lower()

        if applicable_lower == "true":
            applicable = True
        elif applicable_lower == "false":
            applicable = False
        else:
            applicable = None

    if isinstance(qco, str):
        qco = qco.strip().lower() == "true"

    if isinstance(crs, str):
        crs = crs.strip().lower() == "true"

    # Certification applicability is known
    if applicable is False:
        verification_status = "NOT_CERTIFIABLE"
        requirement = "Not Certifiable"
        scheme = None

    elif applicable is True:

        if crs is True:
            verification_status = "VERIFIED"
            requirement = "Mandatory Certification"
            scheme = "CRS"

        elif qco is True:
            verification_status = "VERIFIED"
            requirement = "Mandatory Certification"
            scheme = "QCO"

        elif details and "voluntary" in str(details).lower():
            verification_status = "VERIFIED"
            requirement = "Voluntary Certification"
            scheme = "Voluntary"

        else:
            verification_status = "VERIFIED"
            requirement = "Certification Applicable"
            scheme = None

    # Dataset does not contain enough information
    else:
        verification_status = "REVIEW_REQUIRED"
        requirement = "Information Unavailable"
        scheme = None

    return {
        "applicable": applicable,
        "requirement": requirement,
        "scheme": scheme,
        "qco": qco,
        "crs": crs,
        "details": details,
        "source_available": bool(bis_url),
        "official_bis_source": bis_url,
        "verification_status": verification_status
    }


def get_standard_metadata(standard_id: str) -> dict:
    """
    Retrieve the original BIS metadata for an accepted standard
    from ChromaDB.

    The accepted value may be either:
    - the ChromaDB document ID
    - the BIS IS number stored in metadata
    """

    try:
        # First try exact ChromaDB ID
        result = collection.get(
            ids=[standard_id],
            include=["metadatas", "documents"]
        )

        if result.get("metadatas"):
            metadata = result["metadatas"][0] or {}

            document = ""

            if result.get("documents"):
                document = result["documents"][0] or ""

            metadata["_document"] = document

            return metadata

    except Exception:
        pass

    # If exact ID was not found, search all metadata
    try:
        result = collection.get(
            include=["metadatas", "documents"]
        )

        ids = result.get("ids", [])
        metadatas = result.get("metadatas", [])
        documents = result.get("documents", [])

        for index, metadata in enumerate(metadatas):

            metadata = metadata or {}

            is_number = str(
                metadata.get("is_number", "")
            ).strip()

            if is_number.lower() == str(
                standard_id
            ).strip().lower():

                metadata["_document"] = (
                    documents[index]
                    if index < len(documents)
                    else ""
                )

                return metadata

            # Also check common alternative metadata fields
            metadata_standard = str(
                metadata.get("standard_number", "")
            ).strip()

            if metadata_standard.lower() == str(
                standard_id
            ).strip().lower():

                metadata["_document"] = (
                    documents[index]
                    if index < len(documents)
                    else ""
                )

                return metadata

            # Check the actual Chroma ID as a final fallback
            if index < len(ids):

                if str(ids[index]).strip().lower() == str(
                    standard_id
                ).strip().lower():

                    metadata["_document"] = (
                        documents[index]
                        if index < len(documents)
                        else ""
                    )

                    return metadata

    except Exception:
        pass

    return {}


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):

    # Run existing RAG + LLM analysis
    result = analyze_query(
        query=request.query,
        top_k=request.top_k
    )

    # Get IDs of retrieved standards
    standard_ids = [
        standard["id"]
        for standard in result["standards"]
    ]

    # Run version/amendment check independently
    version_checks = check_versions(standard_ids)

    # Attach version, certification and related standards
    for standard, version_check in zip(
        result["standards"],
        version_checks
    ):

        # ---------------------------------------------------------
        # Version / amendment verification
        # ---------------------------------------------------------

        standard["version_check"] = version_check

        # ---------------------------------------------------------
        # Automatic certification verification
        # ---------------------------------------------------------

        standard["certification_verification"] = (
            build_certification_verification(
                standard.get("metadata", {})
            )
        )

        # ---------------------------------------------------------
        # Find allied / related BIS standards
        # ---------------------------------------------------------

        related_standards = get_related_standards(
            standard["id"]
        )

        standard["related_standards"] = related_standards

    # Record standards analysis in audit trail
    audit_logger.append(
        user_id="officer_001",
        action="standards_analyzed",
        data={
            "query": request.query,
            "num_recommendations": len(result["standards"]),
            "top_k": request.top_k,
            "explanation_generated": True
        }
    )

    return result


@router.post(
    "/accept",
    response_model=AcceptanceResponse
)
async def accept_standards(
    request: AcceptanceRequest
):

    # Officer must verify the standards
    if not request.verified:
        raise HTTPException(
            status_code=400,
            detail="Officer must verify standards before acceptance"
        )

    # Verify certification status for every accepted standard
    for standard in request.accepted_standards:

        if not request.certification_verifications.get(
            standard,
            False
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Certification must be verified for {standard}"
                )
            )

    output_dir = Path(settings.PDF_OUTPUT_DIR)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    pdf_filename = (
        f"bundle_{request.tender_id}_"
        f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    )

    pdf_path = output_dir / pdf_filename

    # ---------------------------------------------------------
    # Build PDF recommendations using actual BIS metadata
    # ---------------------------------------------------------

    recommendations = []

    for std in request.accepted_standards:

        # Retrieve original metadata from ChromaDB
        metadata = get_standard_metadata(std)

        # Build the same automatic certification verification
        # used during analysis
        certification_verification = (
            build_certification_verification(
                metadata
            )
        )

        # Try to get a meaningful title/scope
        standard_title = (
            metadata.get("title")
            or metadata.get("standard_title")
            or metadata.get("scope")
            or metadata.get("document")
            or f"Standard {std}"
        )

        # Try to get category
        category = (
            metadata.get("category")
            or "BIS Standard"
        )

        # Try to get year
        year = metadata.get(
            "year",
            "N/A"
        )

        # Try to get official IS number
        standard_number = (
            metadata.get("is_number")
            or std
        )

        # Get related standards for PDF
        related_standards = get_related_standards(
            std
        )

        # Add complete recommendation
        recommendations.append(
            {
                "standard_number": standard_number,

                "standard_title": standard_title,

                "relevance_score": 85.0,

                "category": category,

                "year": year,

                "status": "Verified",

                "certification": "BIS",

                "why_recommended": (
                    "Selected and verified by the officer."
                ),

                "evidence": (
                    "See official BIS documentation."
                ),

                # Complete automatic certification information
                "certification_verification": (
                    certification_verification
                ),

                # Keep the official BIS source separately
                "official_bis_source": (
                    certification_verification.get(
                        "official_bis_source"
                    )
                ),

                # Related / allied standards
                "related_standards": related_standards,

                # Preserve original metadata
                "metadata": metadata
            }
        )

    # ---------------------------------------------------------
    # Generate PDF bundle
    # ---------------------------------------------------------

    generate_standards_bundle(
        tender_id=request.tender_id,
        officer_id=request.officer_id,
        query="BIS Standards Recommendation",
        recommendations=recommendations,
        output_path=str(pdf_path)
    )

    # ---------------------------------------------------------
    # Record officer acceptance and certification verification
    # ---------------------------------------------------------

    audit_logger.append(
        user_id=request.officer_id,
        action="standards_accepted",
        data={
            "tender_id": request.tender_id,
            "accepted_standards": request.accepted_standards,
            "verified": request.verified,
            "certification_verifications": (
                request.certification_verifications
            )
        }
    )

    # ---------------------------------------------------------
    # Record PDF generation
    # ---------------------------------------------------------

    audit_logger.append(
        user_id=request.officer_id,
        action="pdf_generated",
        data={
            "tender_id": request.tender_id,
            "accepted_standards": request.accepted_standards,
            "certification_verifications": (
                request.certification_verifications
            ),
            "pdf_filename": pdf_filename
        }
    )

    return {
        "status": "accepted",
        "pdf_url": f"/standards/pdf/{pdf_filename}",
        "timestamp": datetime.utcnow()
    }


@router.get("/pdf/{filename}")
async def download_pdf(
    filename: str
):

    pdf_path = (
        Path(settings.PDF_OUTPUT_DIR)
        / filename
    )

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=filename
    )