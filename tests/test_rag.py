"""
ScamTrap AI — Repository RAG Engine Tests (§4.6)
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.rag_engine import rag_engine
from backend.app.services.llm_provider import OllamaLocalProvider, get_llm_provider

client = TestClient(app)


def test_workspace_indexing():
    """Test indexing of workspace files."""
    res = rag_engine.index_workspace(force=True)
    assert res["status"] in ["indexed", "already_indexed"]
    assert res["file_count"] > 0
    assert res["chunk_count"] > 0


def test_vector_retrieval():
    """Test TF-IDF vector retrieval of code chunks."""
    rag_engine.index_workspace()
    results = rag_engine.retrieve("pipeline orchestrator scam dna", top_k=3)
    assert len(results) > 0
    assert "file_path" in results[0]
    assert "relevance_score" in results[0]
    assert results[0]["relevance_score"] >= 0.0


@pytest.mark.asyncio
async def test_rag_query_synthesis():
    """Test full RAG query synthesis with citations."""
    res = await rag_engine.query_rag("How does Scam DNA extraction work?", top_k=3)
    assert "query" in res
    assert "answer" in res
    assert "citations" in res
    assert len(res["citations"]) > 0


@pytest.mark.asyncio
async def test_ollama_local_provider_fallback():
    """Test OllamaLocalProvider graceful fallback when service is offline."""
    ollama = OllamaLocalProvider(base_url="http://localhost:99999", model="llama3")
    answer = await ollama.generate_text("Test prompt")
    assert answer == ""  # Graceful fallback on unreachable port


def test_rag_api_endpoints():
    """Test RAG API gateway endpoints."""
    # Stats
    res = client.get("/api/v1/rag/stats")
    assert res.status_code == 200
    assert res.json()["is_indexed"] is True

    # Index
    res = client.post("/api/v1/rag/index?force=true")
    assert res.status_code == 200

    # Query
    res = client.post("/api/v1/rag/query", json={"query": "Explain incident ingestion", "top_k": 3})
    assert res.status_code == 200
    data = res.json()
    assert "citations" in data
    assert "retrieved_chunks" in data
