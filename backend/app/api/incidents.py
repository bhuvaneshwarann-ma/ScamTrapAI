"""
ScamTrap AI — Incidents API Router (Phase 12)

Endpoints:
- POST /api/v1/incidents
- GET /api/v1/incidents
- GET /api/v1/incidents/{id}
- GET /api/v1/incidents/{id}/dna
- GET /api/v1/incidents/{id}/relationships
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.engine import get_db, init_db
from backend.app.db import crud
from backend.app.models.incident import IncidentCreate, Incident, IncidentSummary
from backend.app.models.scam_dna import ScamDNA
from backend.app.models.relationship import Relationship
from backend.app.services.llm_provider import get_llm_provider
from backend.app.services.relationship_engine import RelationshipEngine

from backend.app.services.pipeline_orchestrator import PipelineOrchestrator

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])
orchestrator = PipelineOrchestrator()


@router.post("", response_model=Incident)
async def create_incident(req: IncidentCreate, db: Session = Depends(get_db)):
    """
    Ingest incident transcript and run full real intelligence pipeline:
    Sanitization -> Scam DNA -> Entity Resolution -> Relationship Engine -> Evidence -> Campaign Detection.
    """
    init_db()

    res = await orchestrator.process_incident(
        db=db,
        raw_text=req.raw_text,
        channel=req.channel,
        reported_by=req.reported_by,
        metadata=req.metadata,
    )

    return res["incident"]


@router.get("", response_model=List[IncidentSummary])
async def list_incidents(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List ingested incidents."""
    init_db()
    items = crud.list_incidents(db, skip=skip, limit=limit)
    summaries = []
    for item in items:
        dna_dict = item.scam_dna or {}
        summaries.append(
            IncidentSummary(
                id=item.id,
                channel=item.channel,
                status=item.status,
                language=dna_dict.get("language"),
                impersonation_target=dna_dict.get("impersonation_target"),
                campaign_id=item.campaign_id,
                created_at=item.created_at,
            )
        )
    return summaries


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str, db: Session = Depends(get_db)):
    """Get single incident by ID."""
    init_db()
    item = crud.get_incident(db, incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")

    dna = ScamDNA(**item.scam_dna) if item.scam_dna else None

    return Incident(
        id=item.id,
        raw_text=item.raw_text,
        channel=item.channel,
        status=item.status,
        scam_dna=dna,
        campaign_id=item.campaign_id,
        ground_truth_campaign_id=item.ground_truth_campaign_id,
        created_at=item.created_at,
    )


@router.get("/{incident_id}/dna", response_model=ScamDNA)
async def get_incident_dna(incident_id: str, db: Session = Depends(get_db)):
    """Get Scam DNA for an incident."""
    init_db()
    item = crud.get_incident(db, incident_id)
    if not item or not item.scam_dna:
        raise HTTPException(status_code=404, detail="Scam DNA not found for incident")
    return ScamDNA(**item.scam_dna)
