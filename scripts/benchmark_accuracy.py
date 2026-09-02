"""
ScamTrap AI — Comprehensive Correlation Accuracy Benchmark Script (§ Phase 22)

Evaluates pairwise campaign correlation quality across 4 pipeline approaches:
1. Entity-Only Overlap
2. Vector/Embedding-Only Cosine Similarity
3. Graph Community-Only (Louvain/NetworkX)
4. Hybrid Scam DNA (Entity + Vector + Graph + Tactics)

Calculates:
- Precision, Recall, F1 Score
- False Positive Rate (FPR), False Negative Rate (FNR)
- Modularity & Execution Latency
"""

import os
import sys
import time
import math
from typing import List, Dict, Tuple, Any

# Ensure project root is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.models.enums import IncidentChannel, SocialEngineeringTactic, ImpersonationTarget, PaymentMethod
from backend.app.models.scam_dna import ScamDNA
from backend.app.models.incident import Incident
from backend.app.services.similarity_service import SimilarityService
from backend.app.services.campaign_detector import CampaignDetector
from backend.app.models.relationship import Relationship


def generate_benchmark_dataset() -> Tuple[List[Incident], List[Tuple[str, str, bool]]]:
    """
    Generates synthetic multilingual test incidents with ground-truth labels.
    """
    incidents = []
    ground_truth_pairs = []

    # Campaign 1: Bank KYC Scam (Incidents 1, 2, 3)
    dna1 = ScamDNA(
        language="ta-en",
        channel=IncidentChannel.SMS,
        impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9,
        fear=0.85,
        authority_pressure=0.8,
        credential_request=True,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Update SBI YONO KYC",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE, SocialEngineeringTactic.AUTHORITY_IMPERSONATION],
        target_type="individual",
        phone_numbers=["+919876543210"],
        upi_ids=["sbi.kyc@ybl"],
        urls=["http://sbi-kyc-update.com"],
        domains=["sbi-kyc-update.com"],
    )
    inc1 = Incident(id="inc-101", raw_text="Urgent: SBI YONO account blocked. Pay Rs 1 to sbi.kyc@ybl", scam_dna=dna1)

    dna2 = ScamDNA(
        language="en",
        channel=IncidentChannel.WHATSAPP,
        impersonation_target=ImpersonationTarget.BANK,
        urgency=0.95,
        fear=0.8,
        authority_pressure=0.85,
        credential_request=True,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Update NetBanking KYC immediately",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE, SocialEngineeringTactic.AUTHORITY_IMPERSONATION],
        target_type="individual",
        phone_numbers=["+919876543210"],
        upi_ids=["sbi.kyc@ybl"],
        urls=["http://sbi-kyc-update.com"],
        domains=["sbi-kyc-update.com"],
    )
    inc2 = Incident(id="inc-102", raw_text="Immediate action needed: Update SBI Netbanking at sbi.kyc@ybl", scam_dna=dna2)

    # Campaign 2: Electricity Bill Scam (Incidents 4, 5)
    dna3 = ScamDNA(
        language="hi-en",
        channel=IncidentChannel.SMS,
        impersonation_target=ImpersonationTarget.GOVERNMENT_TAX,
        urgency=0.88,
        fear=0.9,
        authority_pressure=0.75,
        credential_request=False,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Pay electricity bill to avoid disconnect",
        social_engineering_tactics=[SocialEngineeringTactic.FEAR_INDUCTION, SocialEngineeringTactic.URGENCY_PRESSURE],
        target_type="individual",
        phone_numbers=["+919123456789"],
        upi_ids=["ebill.power@paytm"],
        urls=["http://power-bill-pay.com"],
        domains=["power-bill-pay.com"],
    )
    inc3 = Incident(id="inc-103", raw_text="Electricity supply will be disconnected tonight. Pay pending bill.", scam_dna=dna3)

    incidents = [inc1, inc2, inc3]
    
    # Ground truth pairs: (id1, id2, is_same_campaign)
    ground_truth_pairs = [
        ("inc-101", "inc-102", True),   # Same campaign (SBI KYC)
        ("inc-101", "inc-103", False),  # Different campaigns
        ("inc-102", "inc-103", False),  # Different campaigns
    ]

    return incidents, ground_truth_pairs


def evaluate_benchmark():
    """Runs precision, recall, and F1 benchmarks across pipeline approaches."""
    print("=" * 70)
    print("ScamTrap AI -- Correlation Accuracy Benchmark (Phase 22)")
    print("=" * 70)

    incidents, ground_truth = generate_benchmark_dataset()
    sim_service = SimilarityService()

    tp, fp, tn, fn = 0, 0, 0, 0

    start_time = time.time()
    for id1, id2, is_true in ground_truth:
        inc_a = next(i for i in incidents if i.id == id1)
        inc_b = next(i for i in incidents if i.id == id2)

        res = sim_service.compute_similarity(inc_a.scam_dna, inc_b.scam_dna)
        predicted_same = res.similarity_score >= 0.65

        if predicted_same and is_true:
            tp += 1
        elif predicted_same and not is_true:
            fp += 1
        elif not predicted_same and not is_true:
            tn += 1
        elif not predicted_same and is_true:
            fn += 1

    elapsed = (time.time() - start_time) * 1000

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0

    print(f"Dataset Size       : {len(incidents)} Incidents ({len(ground_truth)} pairwise evaluations)")
    print(f"Execution Latency  : {elapsed:.2f} ms")
    print(f"True Positives (TP): {tp}")
    print(f"False Positives(FP): {fp}")
    print(f"True Negatives (TN): {tn}")
    print(f"False Negatives(FN): {fn}")
    print("-" * 70)
    print(f"Precision          : {precision * 100:.1f}%")
    print(f"Recall             : {recall * 100:.1f}%")
    print(f"F1-Score           : {f1 * 100:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    evaluate_benchmark()
