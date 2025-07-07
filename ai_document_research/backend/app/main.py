from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.logging.logging_config import setup_logging
from app.middlewares.custom_header import add_custom_header
from app.api.routes import router as api_router  # centralized router

# 🔧 Setup Logging
setup_logging()

# 🚀 Initialize FastAPI app
app = FastAPI(
    title=settings.app_name or "AI Document Research + Conversion",
    version=settings.app_version or "1.0.0",
    description="🚀 An API for AI-powered document research and file format conversion.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 🌐 CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧾 Custom Middleware: Add custom headers
app.middleware("http")(add_custom_header)

# 🔌 Include All API Routes from `api/__init__.py`
app.include_router(api_router, prefix="/api")