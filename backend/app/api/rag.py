"""
ScamTrap AI — RAG API Gateway Router (§4.6)
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.rag_engine import rag_engine

rag_router = APIRouter(prefix="/api/v1/rag", tags=["Repository RAG"])


class RAGQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


@rag_router.post("/index")
async def index_repository(force: Optional[bool] = False):
    """Index all repository files for RAG search."""
    try:
        res = rag_engine.index_workspace(force=force)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/query")
async def query_rag_engine(req: RAGQueryRequest):
    """Query the Repository RAG Engine with Local LLM analysis and file citations."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    try:
        res = await rag_engine.query_rag(req.query, top_k=req.top_k or 5)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.get("/stats")
async def get_rag_stats():
    """Get RAG Engine indexing statistics."""
    if not rag_engine.is_indexed:
        rag_engine.index_workspace()
    return {
        "is_indexed": rag_engine.is_indexed,
        "file_count": len(rag_engine.indexed_files),
        "chunk_count": len(rag_engine.chunks),
        "indexed_files_sample": rag_engine.indexed_files[:10],
    }
