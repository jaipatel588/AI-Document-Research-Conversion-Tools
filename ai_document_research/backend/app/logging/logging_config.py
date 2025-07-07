import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config.settings import settings

# ✅ Ensure log_file has a valid string path
log_file = settings.log_file or "logs/app.log"
log_level = (settings.log_level or "INFO").upper()

# ✅ Ensure logs directory exists
log_dir = Path(log_file).parent
log_dir.mkdir(parents=True, exist_ok=True)

def setup_logging():
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # ✅ File handler (rotates after 5MB, keeps 3 backups)
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    # ✅ Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_level)

    # ✅ Root logger setup
    logging.basicConfig(
        level=log_level,
        handlers=[file_handler, console_handler]
    )

    # ✅ Avoid duplicate uvicorn error logs
    logging.getLogger("uvicorn.error").handlers = []