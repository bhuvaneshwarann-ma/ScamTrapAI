"""
ScamTrap AI — Real Evaluation & Calibration API (Phase 14 & 18)

Calculates REAL benchmark metrics by running prediction vs ground truth:
- Relationship precision, recall, F1
- False positive rate
- Campaign detection rate
- False similarity rejection test (explicit check for Incident D / negative control)
"""

import json
from pathlib import Path
from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.engine import get_db, init_db
from backend.app.db import crud
from backend.app.models.enums import IncidentChannel
from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship as RelPydantic
from backend.app.services.llm_provider import MockLLMProvider
from backend.app.services.relationship_engine import RelationshipEngine
from backend.app.services.campaign_detector import CampaignDetector

router = APIRouter(prefix="/api/v1", tags=["evaluation"])


async def _calculate_metrics(db: Session) -> Dict[str, Any]:
    """Calculate real evaluation metrics from DB data or demo dataset."""
    init_db()

    # Load demo scenario or DB incidents
    demo_file = Path(__file__).parent.parent.parent.parent / "data" / "seed" / "demo_scenario.json"
    incidents = []

    if demo_file.exists():
        with open(demo_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        llm = MockLLMProvider()
        for item in data:
            chan = IncidentChannel.SMS if item.get("channel") == "sms" else IncidentChannel.WHATSAPP
            dna = await llm.extract_scam_dna(item["raw_text"], chan)
            inc = Incident(
                id=item["id"],
                raw_text=item["raw_text"],
                channel=chan,
                scam_dna=dna,
                ground_truth_campaign_id=item["ground_truth_campaign_id"],
            )
            incidents.append(inc)

    # If demo file wasn't present, load from DB
    if not incidents:
        db_items = crud.list_incidents(db, skip=0, limit=50)
        from backend.app.models.scam_dna import ScamDNA
        for item in db_items:
            dna = ScamDNA(**item.scam_dna) if item.scam_dna else None
            incidents.append(
                Incident(
                    id=item.id,
                    raw_text=item.raw_text,
                    channel=item.channel,
                    status=item.status,
                    scam_dna=dna,
                    ground_truth_campaign_id=item.ground_truth_campaign_id,
                    created_at=item.created_at,
                )
            )

    engine = RelationshipEngine()
    relationships = []
    for i in range(len(incidents)):
        for j in range(i + 1, len(incidents)):
            rel = engine.evaluate_pair(incidents[i], incidents[j])
            if rel:
                relationships.append(rel)

    # Evaluate ground truth relationship precision/recall
    tp = 0
    fp = 0
    fn = 0

    for rel in relationships:
        inc1 = next((x for x in incidents if x.id == rel.source_incident_id), None)
        inc2 = next((x for x in incidents if x.id == rel.target_incident_id), None)

        if inc1 and inc2:
            same_ground_truth = (
                inc1.ground_truth_campaign_id is not None and
                inc1.ground_truth_campaign_id == inc2.ground_truth_campaign_id and
                "LEGIT" not in inc1.ground_truth_campaign_id
            )

            if rel.is_verified:
                if same_ground_truth:
                    tp += 1
                else:
                    fp += 1
            else:
                if same_ground_truth:
                    fn += 1

    precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 1.0
    recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 1.0
    f1 = round(2 * precision * recall / (precision + recall), 4) if (precision + recall) > 0 else 1.0
    fpr = round(fp / (fp + tp + 1e-5), 4)

    # Campaign detection
    detector = CampaignDetector(min_incidents=2, min_relationship_confidence=0.60)
    detected = detector.detect_campaigns(incidents, relationships)

    # False Similarity Rejection Test: verify Incident D (inc-demo-d or LEGIT) is NOT in any detected campaign
    false_similarity_rejected = True
    for camp, alert in detected:
        if "inc-demo-d" in camp.incident_ids:
            false_similarity_rejected = False
            break
        # Also check ground truth campaign IDs
        gt_ids = {inc.ground_truth_campaign_id for inc in incidents if inc.id in camp.incident_ids}
        if any(g and "LEGIT" in g for g in gt_ids):
            false_similarity_rejected = False
            break

    return {
        "dataset_size": len(incidents),
        "relationship_precision": precision,
        "relationship_recall": recall,
        "relationship_f1": f1,
        "false_positive_rate": fpr,
        "campaign_detection_count": len(detected),
        "false_similarity_rejected": false_similarity_rejected,
    }


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get real, calculated system evaluation metrics."""
    return await _calculate_metrics(db)


@router.post("/evaluation/run")
async def run_evaluation(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Trigger dynamic evaluation run against ground truth."""
    metrics = await _calculate_metrics(db)
    return {
        "status": "completed",
        "scorecard": metrics
    }
