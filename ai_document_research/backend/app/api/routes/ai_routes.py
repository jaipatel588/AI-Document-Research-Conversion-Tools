from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from typing import List
from io import BytesIO
from docx import Document
import fitz
import logging

from app.services.vector_service import (
    build_faiss_index_from_texts,
    search_similar_texts
)
from app.models.schemas import (
    SearchRequest,
    BuildIndexRequest,
    AIResearchResponse,
    ErrorResponse
)

# Initialize router
router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# =============================
# ✅ Build index from JSON body
# =============================
@router.post("/build-index", tags=["AI Document Research"],
             responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def build_index_route(request: BuildIndexRequest):
    if len(request.texts) != len(request.metadata):
        raise HTTPException(status_code=400, detail="❌ Text and metadata counts do not match.")
    
    try:
        build_faiss_index_from_texts(request.texts, request.metadata)
        logger.info("✅ Index built successfully from JSON.")
        return {"message": "✅ Index built successfully."}
    
    except Exception as e:
        logger.error(f"❌ Index build failed: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Index build failed: {str(e)}")


# =============================
# ✅ Build index from uploaded files (.txt, .pdf, .docx)
# =============================
@router.post("/index-files", tags=["AI Document Research"],
             responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def index_documents(files: List[UploadFile] = File(...), metadata: List[str] = Form(...)):
    if len(files) != len(metadata):
        raise HTTPException(status_code=400, detail="❌ Files and metadata count mismatch.")

    texts = []
    MAX_FILE_SIZE_MB = 10

    for file in files:
        filename = file.filename or "unknown"
        try:
            content = await file.read()
            if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise HTTPException(status_code=400, detail=f"❌ File too large (>{MAX_FILE_SIZE_MB}MB): {filename}")

            extension = filename.lower().split('.')[-1]

            # Extract text based on file extension
            if extension == "txt":
                text = content.decode("utf-8")
            elif extension == "pdf":
                with fitz.open(stream=content, filetype="pdf") as doc:
                    text = "\n".join([page.get_text() for page in doc]) # type: ignore
            elif extension == "docx":
                doc = Document(BytesIO(content))
                text = "\n".join([para.text for para in doc.paragraphs])
            else:
                raise HTTPException(status_code=400, detail=f"❌ Unsupported file format: {filename}")

            texts.append(text)
            logger.info(f"✅ Processed file: {filename}")

        except Exception as e:
            logger.error(f"❌ Error processing file {filename}: {e}")
            raise HTTPException(status_code=500, detail=f"❌ Error processing file {filename}: {str(e)}")

    try:
        build_faiss_index_from_texts(texts, metadata)
        logger.info("✅ Documents indexed successfully.")
        return {"message": "✅ Documents indexed successfully."}
    
    except Exception as e:
        logger.error(f"❌ Indexing failed: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Indexing failed: {str(e)}")


# =============================
# ✅ Search using GET query
# =============================
@router.get("/search", tags=["AI Document Research"],
            response_model=AIResearchResponse,
            responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def search_documents(query: str = Query(..., min_length=3), top_k: int = Query(5, ge=1, le=20)):
    if not query.strip():
        raise HTTPException(status_code=400, detail="❌ Query cannot be empty.")

    try:
        results = search_similar_texts(query, top_k)
        if not results or not results["results"]:
            raise HTTPException(status_code=404, detail="❌ No documents found.")

        logger.info(f"✅ Search successful. Query: '{query}', Top K: {top_k}")
        return {
            "matches": results["results"],  # full list of dicts: rank, score, metadata, text
            "answer": results["ai_summary"]
        }

    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Search failed: {str(e)}")


# =============================
# ✅ Search using POST body
# =============================
@router.post("/search-body", tags=["AI Document Research"],
             response_model=AIResearchResponse,
             responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def search_with_body(request: SearchRequest):
    try:
        results = search_similar_texts(request.query, top_k=request.top_k)
        if not results or not results["results"]:
            raise HTTPException(status_code=404, detail="❌ No documents found.")

        logger.info(f"✅ Body search successful. Query: '{request.query}', Top K: {request.top_k}")
        return {
            "matches": results["results"],
            "answer": results["ai_summary"]
        }

    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"❌ Search failed: {str(e)}")