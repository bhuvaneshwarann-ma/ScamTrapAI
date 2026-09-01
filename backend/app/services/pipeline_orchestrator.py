"""
ScamTrap AI — Pipeline Orchestrator

End-to-end intelligence orchestrator connecting:
1. Input Sanitization (§4.1)
2. Scam DNA Extraction
3. Entity Resolution & Mention Linking
4. Incident Persistence
5. Pairwise Relationship Evaluation (ML Probability + Deterministic Corroboration)
6. Evidence Generation & Persistence
7. Campaign Detection & Persistence
8. Campaign Graph Update
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.core.sanitizer import sanitize_input
from backend.app.core.logging import get_logger
from backend.app.db import crud
from backend.app.models.enums import IncidentChannel, EntityType, ProvenanceType
from backend.app.models.incident import Incident
from backend.app.models.scam_dna import ScamDNA
from backend.app.services.llm_provider import get_llm_provider
from backend.app.services.entity_resolver import EntityResolver
from backend.app.services.relationship_engine import RelationshipEngine
from backend.app.services.campaign_detector import CampaignDetector

logger = get_logger(__name__)


class PipelineOrchestrator:
    """Orchestrates end-to-end intelligence processing for an incident."""

    def __init__(self):
        self.llm_provider = get_llm_provider()
        self.entity_resolver = EntityResolver()
        self.relationship_engine = RelationshipEngine()
        self.campaign_detector = CampaignDetector(min_incidents=2, min_relationship_confidence=0.60)

    async def process_incident(
        self,
        db: Session,
        raw_text: str,
        channel: IncidentChannel = IncidentChannel.OTHER,
        reported_by: Optional[str] = None,
        metadata: Optional[dict] = None,
        ground_truth_campaign_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process incident through full intelligence pipeline."""
        # 1. Input Sanitization
        sanitized = sanitize_input(raw_text)

        # 2. Create Incident Record
        inc_db = crud.create_incident(
            db=db,
            raw_text=sanitized.sanitized_text,
            channel=channel.value if hasattr(channel, "value") else str(channel),
            reported_by=reported_by,
            metadata=metadata,
            ground_truth_campaign_id=ground_truth_campaign_id,
        )

        # 3. Scam DNA Extraction
        scam_dna = await self.llm_provider.extract_scam_dna(sanitized.sanitized_text, channel)
        crud.update_incident_scam_dna(db, inc_db.id, scam_dna.model_dump(mode="json"))

        # 4. Entity Extraction & Resolution
        resolved_entities = []
        for phone in scam_dna.phone_numbers:
            mention, entity_model = self.entity_resolver.resolve_mention(phone, EntityType.PHONE, inc_db.id)
            entity_db = crud.get_or_create_entity(db, entity_model.entity_type.value, entity_model.normalized_value, entity_model.resolution_confidence)
            crud.create_entity_mention(db, inc_db.id, entity_model.entity_type.value, phone, entity_db.id)
            resolved_entities.append(entity_db)

        for upi in scam_dna.upi_ids:
            mention, entity_model = self.entity_resolver.resolve_mention(upi, EntityType.UPI, inc_db.id)
            entity_db = crud.get_or_create_entity(db, entity_model.entity_type.value, entity_model.normalized_value, entity_model.resolution_confidence)
            crud.create_entity_mention(db, inc_db.id, entity_model.entity_type.value, upi, entity_db.id)
            resolved_entities.append(entity_db)

        for url in scam_dna.urls:
            mention, entity_model = self.entity_resolver.resolve_mention(url, EntityType.URL, inc_db.id)
            entity_db = crud.get_or_create_entity(db, entity_model.entity_type.value, entity_model.normalized_value, entity_model.resolution_confidence)
            crud.create_entity_mention(db, inc_db.id, entity_model.entity_type.value, url, entity_db.id)
            resolved_entities.append(entity_db)

        # 5. Load Recent Incidents for Relationship Evaluation
        current_inc_model = Incident(
            id=inc_db.id,
            raw_text=inc_db.raw_text,
            channel=channel,
            status=inc_db.status,
            scam_dna=scam_dna,
            ground_truth_campaign_id=inc_db.ground_truth_campaign_id,
            created_at=inc_db.created_at,
        )

        recent_db_incidents = crud.list_incidents(db, skip=0, limit=50)
        previous_incmodels = []
        for item in recent_db_incidents:
            if item.id == inc_db.id or not item.scam_dna:
                continue
            previous_incmodels.append(
                Incident(
                    id=item.id,
                    raw_text=item.raw_text,
                    channel=item.channel,
                    status=item.status,
                    scam_dna=ScamDNA(**item.scam_dna),
                    ground_truth_campaign_id=item.ground_truth_campaign_id,
                    created_at=item.created_at,
                )
            )

        # 6. Evaluate Pairwise Relationships & Persist
        created_relationships = []
        for prev_inc in previous_incmodels:
            rel = self.relationship_engine.evaluate_pair(current_inc_model, prev_inc)
            if rel:
                rel_db = crud.create_relationship(
                    db=db,
                    source_incident_id=rel.source_incident_id,
                    target_incident_id=rel.target_incident_id,
                    relationship_type=rel.relationship_type.value if hasattr(rel.relationship_type, "value") else str(rel.relationship_type),
                    relationship_probability=rel.relationship_probability,
                    relationship_confidence=rel.relationship_confidence,
                    supporting_evidence=[e.model_dump(mode="json") for e in rel.supporting_evidence],
                    feature_contributions=rel.feature_contributions,
                    explanation=rel.explanation,
                    is_verified=rel.is_verified,
                )

                # Persist Evidence
                for ev in rel.supporting_evidence:
                    crud.create_evidence(
                        db=db,
                        claim=ev.claim,
                        evidence_type=ev.type.value if hasattr(ev.type, "value") else str(ev.type),
                        source=ev.source,
                        evidence_confidence=ev.evidence_confidence,
                        relationship_id=rel_db.id,
                        supporting_incident_ids=ev.supporting_incident_ids,
                        supporting_entity_ids=ev.supporting_entity_ids,
                        scoring_factors=ev.scoring_factors,
                    )
                created_relationships.append(rel)

        # 7. Run Campaign Detector & Persist
        all_incidents = previous_incmodels + [current_inc_model]
        all_db_rels = crud.list_relationships(db, limit=200)
        from backend.app.models.relationship import Relationship as RelPydantic
        all_pydantic_rels = []
        for r in all_db_rels:
            all_pydantic_rels.append(
                RelPydantic(
                    id=r.id,
                    source_incident_id=r.source_incident_id,
                    target_incident_id=r.target_incident_id,
                    relationship_type=r.relationship_type,
                    relationship_probability=r.relationship_probability,
                    relationship_confidence=r.relationship_confidence,
                    is_verified=r.is_verified,
                )
            )

        detected_campaigns = self.campaign_detector.detect_campaigns(all_incidents, all_pydantic_rels)

        active_campaign_id = None
        for campaign_model, alert in detected_campaigns:
            # Create or update DB campaign
            c_db = crud.create_campaign(
                db=db,
                name=campaign_model.name,
                status=campaign_model.status.value if hasattr(campaign_model.status, "value") else str(campaign_model.status),
                campaign_confidence=campaign_model.campaign_confidence,
                risk_level=campaign_model.risk_level.value if hasattr(campaign_model.risk_level, "value") else str(campaign_model.risk_level),
            )
            for i_id in campaign_model.incident_ids:
                crud.assign_incident_to_campaign(db, i_id, c_db.id)
                if i_id == inc_db.id:
                    active_campaign_id = c_db.id

        return {
            "incident": current_inc_model,
            "scam_dna": scam_dna,
            "resolved_entities": [e.normalized_value for e in resolved_entities],
            "relationships_count": len(created_relationships),
            "campaign_id": active_campaign_id,
            "sanitizer": {
                "is_safe": sanitized.is_safe,
                "detected_threats": sanitized.detected_patterns,
            },
        }
