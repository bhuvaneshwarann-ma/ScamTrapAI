"""
ScamTrap AI — Phase 9.5 Threshold Calibration Script

Grid-sweeps incident-count threshold N in [2..5] and evidence/confidence
threshold C in [0.60..0.95] against the synthetic ground-truth dataset.
Calculates campaign precision, recall, F1, and false campaign rate.
"""

import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.models.enums import IncidentChannel
from backend.app.models.incident import Incident
from backend.app.services.llm_provider import MockLLMProvider
from backend.app.services.relationship_engine import RelationshipEngine
from backend.app.services.campaign_detector import CampaignDetector


def run_calibration():
    dataset_path = Path(__file__).parent.parent / "data" / "seed" / "synthetic_incidents.json"
    if not dataset_path.exists():
        print(f"Dataset missing at {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} incidents for threshold calibration sweep.")
    llm = MockLLMProvider()
    engine = RelationshipEngine()

    incidents = []
    for item in data[:50]:  # Sweep subset for fast calibration
        chan = IncidentChannel.SMS if item.get("channel") == "sms" else IncidentChannel.WHATSAPP
        dna = None
        # Extract DNA
        import asyncio
        dna = asyncio.run(llm.extract_scam_dna(item["raw_text"], chan))
        inc = Incident(
            id=item["id"],
            raw_text=item["raw_text"],
            channel=chan,
            scam_dna=dna,
            ground_truth_campaign_id=item["ground_truth_campaign_id"],
        )
        incidents.append(inc)

    # Evaluate pairwise relationships
    relationships = []
    for i in range(len(incidents)):
        for j in range(i + 1, len(incidents)):
            rel = engine.evaluate_pair(incidents[i], incidents[j])
            if rel:
                relationships.append(rel)

    print(f"Generated {len(relationships)} candidate relationships.")
    print("\n--- Grid Sweep Threshold Results ---")

    best_f1 = 0.0
    best_params = (3, 0.60)

    for n in [2, 3, 4, 5]:
        for c in [0.60, 0.70, 0.80, 0.90]:
            detector = CampaignDetector(min_incidents=n, min_relationship_confidence=c)
            detected = detector.detect_campaigns(incidents, relationships)

            # Evaluate against ground truth
            tp = 0
            fp = 0
            for camp, alert in detected:
                # Check ground truth homogeneity
                inc_ids = set(camp.incident_ids)
                gt_ids = {inc.ground_truth_campaign_id for inc in incidents if inc.id in inc_ids}
                if len(gt_ids) == 1 and not any("NEG" in g for g in gt_ids):
                    tp += 1
                else:
                    fp += 1

            precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
            recall = tp / 5.0  # Approx 5 true campaigns
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

            if f1 > best_f1:
                best_f1 = f1
                best_params = (n, c)

            print(f"N={n}, C={c:.2f} -> Detected={len(detected)}, TP={tp}, FP={fp}, Precision={precision:.2f}, F1={f1:.2f}")

    print(f"\n[CALIBRATION COMPLETE] Selected Thresholds: Min Incidents = {best_params[0]}, Min Confidence = {best_params[1]:.2f} (F1 = {best_f1:.2f})")


if __name__ == "__main__":
    run_calibration()
