from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
import logging

from app.config.settings import settings
from app.services.conversion_service import handle_conversion_to_format
from app.models.schemas import StandardResponse, ErrorResponse

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_FORMATS = {"pdf", "txt", "docx", "jpg", "png"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def cleanup_files(paths: list[Path]):
    for path in paths:
        try:
            if path.exists():
                path.unlink()
                logger.info(f"🧹 Deleted file: {path.name}")
        except Exception as e:
            logger.warning(f"⚠️ Cleanup failed for {path.name}: {e}")

@router.post(
    "/convert",
    summary="Convert a document to a selected format",
    tags=["Document Conversion"],
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    }
)
async def convert_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target_format: str = Form(..., description="Target format: pdf, txt, docx, jpg, png")
):
    target_format = target_format.lower()

    if target_format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail=f"❌ Unsupported target format: {target_format}")

    input_filename = f"{uuid.uuid4().hex}_{file.filename}"
    temp_input_path = settings.upload_dir / input_filename

    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="❌ File size exceeds 20MB limit.")
        with open(temp_input_path, "wb") as buffer:
            buffer.write(contents)
        logger.info(f"📥 Uploaded file saved: {temp_input_path.name}")
    except Exception as e:
        logger.error(f"❌ Failed to save uploaded file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    try:
        output_path = handle_conversion_to_format(temp_input_path, target_format)

        if not output_path or not output_path.exists():
            raise HTTPException(status_code=500, detail="❌ Conversion failed.")

        logger.info(f"✅ File converted successfully: {output_path.name}")
        background_tasks.add_task(cleanup_files, [temp_input_path, output_path])

        return FileResponse(
            path=output_path,
            filename=output_path.name,
            media_type="application/octet-stream"
        )

    except Exception as e:
        logger.error(f"❌ Conversion error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during conversion.")