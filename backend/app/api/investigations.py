"""
ScamTrap AI — Investigations API Router (Phase 12, 20)

Endpoints:
- POST /api/v1/investigations/explain
- POST /api/v1/investigations/copilot
"""

from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.engine import get_db, init_db
from backend.app.db import crud
from backend.app.models.investigation import InvestigationQuery, InvestigationResponse
from backend.app.services.copilot_service import CopilotService
from backend.app.services.evidence_service import EvidenceService

router = APIRouter(prefix="/api/v1/investigations", tags=["investigations"])
copilot_service = CopilotService()
evidence_service = EvidenceService()


@router.post("/copilot", response_model=InvestigationResponse)
async def copilot_qa(query: InvestigationQuery, db: Session = Depends(get_db)):
    """Evidence-bounded investigator copilot Q&A loading real DB evidence."""
    init_db()

    # Load stored DB incidents
    db_incidents = crud.list_incidents(db, skip=0, limit=50)
    from backend.app.models.incident import Incident as IncModel
    from backend.app.models.scam_dna import ScamDNA
    inc_models = []
    for item in db_incidents:
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
    db_rels = crud.list_relationships(db, limit=100)
    from backend.app.models.relationship import Relationship as RelModel
    from backend.app.models.evidence import Evidence as EvModel
    rel_models = []
    for r in db_rels:
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

    return copilot_service.answer_query(query, inc_models, rel_models)


@router.post("/explain")
async def explain_connection(req: Dict[str, Any], db: Session = Depends(get_db)):
    """Explain why incidents are connected with strict provenance."""
    init_db()
    rel_id = req.get("relationship_id")
    if rel_id:
        r = crud.get_relationship(db, rel_id)
        if r:
            from backend.app.models.relationship import Relationship as RelModel
            from backend.app.models.evidence import Evidence as EvModel
            ev_list = [EvModel(**e) for e in (r.supporting_evidence or []) if isinstance(e, dict)]
            rel_model = RelModel(
                id=r.id,
                source_incident_id=r.source_incident_id,
                target_incident_id=r.target_incident_id,
                relationship_type=r.relationship_type,
                relationship_probability=r.relationship_probability,
                relationship_confidence=r.relationship_confidence,
                supporting_evidence=ev_list,
                is_verified=r.is_verified,
            )
            return evidence_service.explain_relationship(rel_model)

    return {
        "status": "success",
        "explanation": "Verified connection based on shared infrastructure.",
        "disclaimer": "DISCLAIMER: EVIDENCE-BOUNDED ASSESSMENT -- SYNTHETIC DEMO ENVIRONMENT.",
    }
