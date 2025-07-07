from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from pathlib import Path


# Base directory pointing to backend/app
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # ==== APP METADATA ====
    app_name: str = "AI Document Research + Conversion API"
    app_version: str = "1.0.0"

    # ==== CORS SETTINGS ====
    cors_origins: List[str] = Field(default=["http://localhost:5173", "http://127.0.0.1:5173"])

    # ==== FILE STORAGE PATHS ====
    upload_dir: Path = Field(default=BASE_DIR / "data" / "uploads")
    convert_dir: Path = Field(default=BASE_DIR / "data" / "converted")
    processed_dir: Path = Field(default=BASE_DIR / "data" / "processed")
    doc_store_path: Path = Field(default=BASE_DIR / "data" / "doc_store.txt")

    # ==== OPENAI API ====
    openai_api_key: str = Field(..., min_length=20, description="Must be set in .env")

    # ==== VECTOR INDEX PATHS ====
    vector_index_path: Path = Field(default=BASE_DIR / "data" / "vector_index.index")
    vector_metadata_path: Path = Field(default=BASE_DIR / "data" / "vector_metadata.json")

    # ==== LOGGING ====
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    # ==== ENVIRONMENT ====
    environment: str = "development"

    # ==== OCR ====
    tesseract_path: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # ==== Limits & Validation ====
    max_upload_size_mb: int = 20
    allowed_conversion_formats: List[str] = ["pdf", "txt", "docx", "jpg", "png"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate settings singleton
settings = Settings() # type: ignore

# Ensure required folders exist
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.convert_dir.mkdir(parents=True, exist_ok=True)
settings.processed_dir.mkdir(parents=True, exist_ok=True)