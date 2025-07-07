from fastapi import APIRouter

from .upload_routes import router as upload_router
from .conversion_routes import router as conversion_router
from .ai_routes import router as ai_research_router
from .health_routes import router as health_router

router = APIRouter()

# Include all routes with clear prefixes and organized tags
router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(conversion_router, prefix="/convert", tags=["Document Conversion"])
router.include_router(ai_research_router, prefix="/ai", tags=["AI Document Research"])