from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.post("/extract")
async def extract_pdf_text(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    try:
        pdf_bytes = await file.read()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        page_count = len(document)

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        document.close()

        extracted_text = extracted_text.strip()

        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No selectable text was found in this PDF. "
                    "Scanned/image-only PDFs are not currently supported."
                )
            )

        return {
            "filename": file.filename,
            "text": extracted_text,
            "pages": page_count
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to extract text from PDF: {str(e)}"
        )