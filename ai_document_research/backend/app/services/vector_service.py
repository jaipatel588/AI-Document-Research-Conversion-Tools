# backend/app/services/vector_service.py

from pathlib import Path
from typing import List, Dict
import numpy as np
import json
import os
import logging
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from app.config.settings import settings

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or settings.openai_api_key)

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Constants
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-3.5-turbo"
INDEX_PATH = Path(os.getenv("VECTOR_INDEX_PATH", settings.vector_index_path))
METADATA_PATH = Path(os.getenv("VECTOR_METADATA_PATH", settings.vector_metadata_path))
DOC_STORE_PATH = settings.doc_store_path
INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

# SentenceTransformer (offline fallback model)
offline_model = SentenceTransformer("all-MiniLM-L6-v2")

# =====================================
# ✅ Embed Text (OpenAI + Offline Fallback)
# =====================================
def embed_text(text: str) -> List[float]:
    try:
        logger.debug("🔍 Generating embedding via OpenAI...")
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        logger.warning(f"⚠️ OpenAI failed: {e} — falling back to SentenceTransformer.")
        try:
            return offline_model.encode(text).tolist()
        except Exception as fallback_error:
            logger.error(f"❌ Fallback embedding failed: {fallback_error}")
            raise

# ======================================
# ✅ AI Answer (OpenAI + Local Fallback)
# ======================================
def generate_ai_answer(query: str, context_docs: List[str]) -> str:
    context = "\n".join(context_docs)
    prompt = f"""You are a helpful assistant. Use only the below context to answer the query:

Context:
{context}

Query:
{query}

Respond with a clear, concise answer."""

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()  # type: ignore

    except Exception as e:
        logger.error(f"❌ Failed to generate AI answer: {e}")
        return generate_local_summary(query, context_docs)

# ======================================
# ✅ Local Fallback Summary Generator
# ======================================
def generate_local_summary(query: str, context_docs: List[str]) -> str:
    if not context_docs:
        return "❌ No context available to generate an answer."

    fallback_answer = "\n\n".join([f"🔹 {doc}" for doc in context_docs[:3]])
    return f"⚠️ AI unavailable. Here are top relevant texts:\n\n{fallback_answer}"

# ======================================
# ✅ Build FAISS Index
# ======================================
def build_faiss_index_from_texts(texts: List[str], metadata: List[str]) -> None:
    if len(texts) != len(metadata):
        raise ValueError("❌ Text and metadata counts do not match.")

    logger.info("🧠 Building FAISS index...")
    embeddings = []
    valid_metadata = []

    try:
        dim = len(embed_text("dimension test"))
        index = faiss.IndexFlatL2(dim)
    except Exception as e:
        logger.error(f"❌ FAISS init error: {e}")
        raise

    for i, text in enumerate(texts):
        try:
            emb = embed_text(text)
            embeddings.append(emb)
            valid_metadata.append(metadata[i])
        except Exception as e:
            logger.warning(f"⚠️ Skipped doc {i} due to error: {e}")

    if not embeddings:
        raise ValueError("❌ No valid embeddings generated.")

    np_embeddings = np.array(embeddings, dtype=np.float32)
    index.add(np.ascontiguousarray(np_embeddings))  # type: ignore

    faiss.write_index(index, str(INDEX_PATH))
    logger.info(f"✅ FAISS index saved to: {INDEX_PATH}")

    with METADATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(valid_metadata, f, indent=2)

    with DOC_STORE_PATH.open("w", encoding="utf-8") as f:
        for doc in texts[:len(valid_metadata)]:
            f.write(doc.replace("\n", " ") + "\n")

# ======================================
# ✅ Search FAISS
# ======================================
def search_similar_texts(query: str, top_k: int = 5) -> Dict:
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("❌ FAISS index or metadata missing.")

    try:
        index = faiss.read_index(str(INDEX_PATH))
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            metadata = json.load(f)

        with DOC_STORE_PATH.open("r", encoding="utf-8") as f:
            docs = f.readlines()

        query_vector = embed_text(query)
        distances, indices = index.search(np.array([query_vector], dtype=np.float32), top_k)

        matched_docs = []
        for rank, idx in enumerate(indices[0]):
            if idx < len(metadata):
                matched_docs.append({
                    "rank": rank + 1,
                    "score": float(distances[0][rank]),
                    "metadata": metadata[idx],
                    "text": docs[idx].strip()
                })

        logger.info(f"🔍 Found {len(matched_docs)} relevant docs.")

        ai_summary = generate_ai_answer(query, [doc["text"] for doc in matched_docs])

        return {
            "query": query,
            "results": matched_docs,
            "ai_summary": ai_summary
        }

    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        return {
            "query": query,
            "results": [],
            "ai_summary": "⚠️ AI summary generation failed due to internal error."
        }