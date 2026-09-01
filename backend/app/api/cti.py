"""
ScamTrap AI — Cyber Threat Intelligence (CTI) API Router

Endpoints:
- GET /api/v1/cti/ioc-search?query={q}
- GET /api/v1/cti/mitre-matrix
- GET /api/v1/cti/threat-feeds
"""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.db.engine import get_db, init_db
from backend.app.services.ioc_search_service import IOCSearchService
from backend.app.services.mitre_mapper import MitreMapper

router = APIRouter(prefix="/api/v1/cti", tags=["cti"])
ioc_service = IOCSearchService()
mitre_service = MitreMapper()


@router.get("/ioc-search")
async def search_ioc(query: str = Query(..., min_length=2), db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Unified IOC search endpoint querying across DB entities, relationships, and threat feeds."""
    init_db()
    result = ioc_service.search_ioc(db, query)
    return result.model_dump(mode="json") if result else {}


@router.get("/mitre-matrix")
async def get_mitre_matrix() -> Dict[str, Any]:
    """Get full MITRE ATT&CK Heatmap Matrix payload for active campaigns."""
    matrix = mitre_service.get_full_matrix()
    return matrix.model_dump(mode="json")


@router.get("/threat-feeds")
async def get_threat_feeds() -> List[Dict[str, Any]]:
    """Get real-time CTI threat feed entries and OSINT blocklists."""
    feeds = ioc_service.get_threat_feeds()
    return [f.model_dump(mode="json") for f in feeds]
