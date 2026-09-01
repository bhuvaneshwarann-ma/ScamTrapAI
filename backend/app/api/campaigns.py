"""
ScamTrap AI — Campaigns API Router (Phase 12)

Endpoints:
- GET /api/v1/campaigns
- GET /api/v1/campaigns/{id}
- GET /api/v1/campaigns/{id}/graph
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.engine import get_db, init_db
from backend.app.db import crud
from backend.app.models.campaign import CampaignSummary, Campaign
from backend.app.services.graph_engine import GraphEngine

router = APIRouter(prefix="/api/v1/campaigns", tags=["campaigns"])


@router.get("", response_model=List[CampaignSummary])
async def list_campaigns(db: Session = Depends(get_db)):
    """List all detected campaigns."""
    init_db()
    camps = crud.list_campaigns(db)
    summaries = []
    for c in camps:
        incidents = crud.get_campaign_incidents(db, c.id)
        summaries.append(
            CampaignSummary(
                id=c.id,
                name=c.name,
                status=c.status,
                incident_count=len(incidents),
                campaign_confidence=c.campaign_confidence,
                risk_level=c.risk_level,
                first_seen=c.first_seen,
                last_seen=c.last_seen,
            )
        )
    return summaries


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str, db: Session = Depends(get_db)):
    """Get single campaign details."""
    init_db()
    c = crud.get_campaign(db, campaign_id)
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")

    incidents = crud.get_campaign_incidents(db, campaign_id)
    return Campaign(
        id=c.id,
        name=c.name,
        status=c.status,
        incident_ids=[i.id for i in incidents],
        campaign_confidence=c.campaign_confidence,
        risk_level=c.risk_level,
        first_seen=c.first_seen,
        last_seen=c.last_seen,
    )


@router.get("/{campaign_id}/graph")
async def get_campaign_graph(campaign_id: str, db: Session = Depends(get_db)):
    """Get React Flow compatible graph JSON for campaign visualization with real stored DB entities and edges."""
    init_db()
    c = crud.get_campaign(db, campaign_id)
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")

    incidents_db = crud.get_campaign_incidents(db, campaign_id)
    if not incidents_db:
        incidents_db = crud.list_incidents(db, skip=0, limit=50)

    # Convert DB incidents to Pydantic models
    from backend.app.models.incident import Incident as IncModel
    from backend.app.models.scam_dna import ScamDNA
    inc_models = []
    for item in incidents_db:
        dna = ScamDNA(**item.scam_dna) if item.scam_dna else None
        inc_models.append(
            IncModel(
                id=item.id,
                raw_text=item.raw_text,
                channel=item.channel,
                status=item.status,
                scam_dna=dna,
                ground_truth_campaign_id=item.ground_truth_campaign_id,
                created_at=item.created_at,
            )
        )

    # Load stored DB relationships
    rels_db = crud.list_relationships(db, limit=200)
    from backend.app.models.relationship import Relationship as RelModel
    from backend.app.models.evidence import Evidence as EvModel
    rel_models = []
    for r in rels_db:
        ev_list = []
        if r.supporting_evidence:
            for ev in r.supporting_evidence:
                if isinstance(ev, dict):
                    ev_list.append(EvModel(**ev))
        rel_models.append(
            RelModel(
                id=r.id,
                source_incident_id=r.source_incident_id,
                target_incident_id=r.target_incident_id,
                relationship_type=r.relationship_type,
                relationship_probability=r.relationship_probability,
                relationship_confidence=r.relationship_confidence,
                supporting_evidence=ev_list,
                is_verified=r.is_verified,
            )
        )

    engine = GraphEngine()
    engine.build_graph(inc_models, rel_models)
    return engine.to_react_flow_json()
