from pathlib import Path
from PIL import Image, UnidentifiedImageError
import pytesseract
import os
import platform
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Setup Tesseract path for Windows
if platform.system().lower() == "windows":
    tesseract_path = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    tesseract_path = Path(tesseract_path).resolve()

    if not tesseract_path.exists():
        logger.warning(f"⚠️ Tesseract not found at {tesseract_path}. OCR will fail if not installed.")
    pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)

def extract_text_from_image(image_path: Path) -> str:
    """Extract text from image using Tesseract OCR."""
    try:
        logger.info(f"🖼️ OCR started on image: {image_path.name}")
        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image).strip()

        if not text:
            logger.warning(f"⚠️ No text found in image: {image_path.name}")
            return ""

        logger.info(f"✅ OCR complete — {len(text)} characters extracted from {image_path.name}")
        return text

    except UnidentifiedImageError:
        logger.error(f"❌ Cannot identify image file: {image_path.name}")
        return ""

    except Exception as e:
        logger.error(f"❌ OCR failed for {image_path.name}: {e}")
        return ""