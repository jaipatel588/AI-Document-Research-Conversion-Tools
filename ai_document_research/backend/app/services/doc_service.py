from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document
from app.services.ocr_service import extract_text_from_image
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = Document(str(file_path))
        paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        logger.error(f"❌ DOCX parsing error ({file_path.name}): {e}")
        return ""

def extract_text_from_txt(file_path: Path) -> str:
    """Extract text from a TXT file."""
    try:
        return file_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        logger.error(f"❌ TXT read error ({file_path.name}): {e}")
        return ""

def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        reader = PdfReader(str(file_path))
        text = "\n".join((page.extract_text() or "").strip() for page in reader.pages)
        return text
    except Exception as e:
        logger.error(f"❌ PDF parsing error ({file_path.name}): {e}")
        return ""

def handle_uploaded_file(file_path: Path) -> str:
    """Detect file type, extract text, and store it in processed folder."""
    ext = file_path.suffix.lower()
    text = ""

    logger.info(f"📄 Processing file: {file_path.name}")

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in {".png", ".jpg", ".jpeg"}:
        text = extract_text_from_image(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        text = extract_text_from_txt(file_path)
    else:
        msg = f"❌ Unsupported file type: {ext}"
        logger.warning(msg)
        return msg

    if not text.strip():
        msg = f"⚠️ No text extracted from: {file_path.name}"
        logger.warning(msg)
        return msg

    # Save extracted text
    try:
        output_dir = file_path.parent.parent / "processed"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{file_path.stem}.txt"
        output_file.write_text(text, encoding="utf-8")

        logger.info(f"✅ Text extracted and saved: {output_file.name}")
        return text
    except Exception as e:
        logger.error(f"❌ Failed to save extracted text: {e}")
        return text + "\n\n⚠️ Text extracted but not saved to file."