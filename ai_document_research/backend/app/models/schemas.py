from pydantic import BaseModel, Field
from typing import List, Optional, Any


class SearchRequest(BaseModel):
    """
    Schema for searching similar texts using a query string and top_k results.
    """
    query: str = Field(
        ..., 
        description="Search query string."
    )
    top_k: int = Field(
        default=5,
        gt=0,
        le=20,
        description="Top-K similar results to return."
    )


class BuildIndexRequest(BaseModel):
    """
    Schema for building a FAISS index from a list of texts and corresponding metadata.
    """
    texts: List[str] = Field(
        ..., 
        description="List of raw document texts."
    )
    metadata: List[str] = Field(
        ..., 
        description="Metadata identifiers for the texts."
    )


class StandardResponse(BaseModel):
    """
    Standard structure for successful API responses.
    """
    message: str = Field(..., description="Result message or status.")
    data: Optional[Any] = Field(default_factory=dict, description="Optional data payload.")


class ErrorResponse(BaseModel):
    """
    Standard structure for error responses.
    """
    detail: str = Field(..., description="Detailed error message or reason.")


class AIResearchResponse(BaseModel):
    """
    Response structure for AI-powered document research.
    """
    matches: List[str] = Field(..., description="Top similar document matches from FAISS index.")
    answer: str = Field(..., description="OpenAI-generated summary or answer based on matched documents.")