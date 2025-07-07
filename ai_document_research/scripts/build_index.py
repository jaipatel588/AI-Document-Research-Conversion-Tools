from pathlib import Path
import json
from backend.app.services.vector_service import build_faiss_index_from_texts
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
# -------------------------------
# ✅ File Paths
# -------------------------------
DATA_DIR = Path("backend/data")
DOC_STORE_FILE = DATA_DIR / "doc_store.txt"
METADATA_FILE = DATA_DIR / "metadata.json"

# -------------------------------
# ✅ Load Documents
# -------------------------------
def load_documents() -> list[str]:
    if not DOC_STORE_FILE.exists():
        raise FileNotFoundError(f"❌ Document file not found: {DOC_STORE_FILE}")
    with DOC_STORE_FILE.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# -------------------------------
# ✅ Load Metadata
# -------------------------------
def load_metadata() -> list[str]:
    if not METADATA_FILE.exists():
        raise FileNotFoundError(f"❌ Metadata file not found: {METADATA_FILE}")
    with METADATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------
# ✅ Main Runner
# -------------------------------
if __name__ == "__main__":
    print("📦 Loading documents and metadata...")
    documents = load_documents()
    metadata = load_metadata()

    print(f"📄 Documents loaded: {len(documents)}")
    print(f"🧾 Metadata entries: {len(metadata)}")

    print("🚀 Building FAISS index...")
    build_faiss_index_from_texts(documents, metadata)
    print("✅ All done!")