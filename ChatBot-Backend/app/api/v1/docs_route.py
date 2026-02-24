from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.docs import DocsUpdateRequest, DocsResponse
from app.services.docs_service import update_docs
from app.services.file_extraction_service import FileTextExtractionService

router = APIRouter(prefix="/docs", tags=["Documents"])


@router.post("/update", response_model=DocsResponse)
def update_documents(payload: DocsUpdateRequest):
    update_docs(payload.content)
    return DocsResponse(
        status="success",
        message="Documents updated & indexed successfully"
    )


@router.post("/upload", response_model=DocsResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        text = FileTextExtractionService.extract(
            file_bytes=file_bytes,
            filename=file.filename
        )

        update_docs(text)

        return DocsResponse(
            status="success",
            message=f"{file.filename} uploaded & indexed successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to process uploaded file"
        )