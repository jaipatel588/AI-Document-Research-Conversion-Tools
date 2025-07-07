from fastapi import APIRouter
from app.models.schemas import StandardResponse

router = APIRouter()


@router.get(
    "/",
    tags=["Health"],
    summary="Check if the API is running",
    response_model=StandardResponse
)
async def health_check():
    return {
        "message": "✅ API is running fine.",
        "data": {
            "version": "1.0.0",
            "description": "AI Document Research & Conversion API is healthy and operational."
        }
    }