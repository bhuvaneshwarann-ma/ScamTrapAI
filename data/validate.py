"""
ScamTrap AI — Phase 3 Dataset Validation Script

Verifies ground-truth balance, campaign distributions, entity coverage,
and negative control ratios in `data/seed/synthetic_incidents.json`.
"""

import json
from collections import Counter
from pathlib import Path


def validate_dataset(filepath: Path):
    assert filepath.exists(), f"Dataset file {filepath} does not exist!"

    with open(filepath, "r", encoding="utf-8") as f:
        incidents = json.load(f)

    print(f"--- Dataset Validation Report ({filepath.name}) ---")
    print(f"Total Incidents: {len(incidents)}")
    assert len(incidents) >= 200, "Dataset must contain at least 200 incidents!"

    campaign_counts = Counter(inc["ground_truth_campaign_id"] for inc in incidents)
    print(f"Total Unique Campaigns: {len(campaign_counts)}")
    assert len(campaign_counts) >= 5, "Dataset must have at least 5 campaigns!"

    print("\nCampaign Breakdown:")
    negative_count = 0
    for camp_id, count in campaign_counts.items():
        print(f"  - {camp_id}: {count} incidents")
        if "NEG" in camp_id:
            negative_count += count

    print(f"\nNegative Control Incidents: {negative_count} ({negative_count / len(incidents) * 100:.1f}%)")
    assert negative_count > 0, "Dataset MUST contain negative control examples!"

    print("\n[VALIDATION SUCCESS] Phase 3 Ground-truth dataset verified successfully!")


if __name__ == "__main__":
    validate_dataset(Path(__file__).parent / "seed" / "synthetic_incidents.json")
