import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def delete_file(path: str):
    try:
        file_path = Path(path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"🗑️ Deleted file: {file_path}")
        else:
            logger.warning(f"⚠️ File not found for deletion: {file_path}")
    except Exception as e:
        logger.error(f"❌ Error deleting file {path}: {e}")