from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
import logging

from app.services.doc_service import handle_uploaded_file
from app.config.settings import settings
from app.models.schemas import StandardResponse, ErrorResponse

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".docx", ".txt"}


@router.post(
    "/document",
    tags=["Upload"],
    summary="Upload a document and extract its text",
    response_model=StandardResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="❌ No filename provided.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"❌ Unsupported file type: {ext}")

    filename = f"{Path(file.filename).stem}_{uuid.uuid4().hex}{ext}"
    file_path = settings.upload_dir / filename

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        logger.info(f"📁 Uploaded file saved: {file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to save file: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Failed to save file: {e}")

    try:
        extracted_text = handle_uploaded_file(file_path)
        return {
            "message": "✅ File uploaded and processed.",
            "data": {
                "filename": filename,
                "extracted_text": extracted_text
            }
        }
    except Exception as e:
        logger.error(f"❌ Failed to process file: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Failed to process file: {e}")