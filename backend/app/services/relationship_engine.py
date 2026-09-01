"""
ScamTrap AI — Hybrid Campaign Relationship Engine (Phase 7)

Combines:
1. ML Candidate Generation -> relationship_probability
2. Deterministic Evidence Verification -> relationship_confidence + Evidence records

Hard architectural rule (§3.2, Phase 7):
ML probability ALONE can never create an investigator-visible high-confidence relationship.
Independent, deterministic corroboration (shared infrastructure, exact taxonomy match)
is strictly required to produce relationship_confidence > 0.60.
"""

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from backend.app.models.enums import (
    ProvenanceType,
    RelationshipType,
)
from backend.app.models.evidence import Evidence
from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship
from backend.app.services.similarity_service import SimilarityService


class RelationshipEngine:
    """Hybrid ML + Deterministic verification relationship engine."""

    def __init__(self):
        self.similarity_service = SimilarityService()

    def evaluate_pair(self, inc1: Incident, inc2: Incident) -> Optional[Relationship]:
        """
        Evaluate candidate relationship between two incidents.
        Returns a Relationship object populated with both probability and confidence.
        """
        if inc1.id == inc2.id:
            return None

        # ── 1. Candidate Generation (ML / Statistical) ────────────────────
        ml_prob = 0.0
        feature_contributions = {}
        dna_sim = 0.0

        if inc1.scam_dna and inc2.scam_dna:
            sim_res = self.similarity_service.compute_similarity(inc1.scam_dna, inc2.scam_dna)
            dna_sim = sim_res.similarity_score
            ml_prob += dna_sim * 0.50
            feature_contributions["scam_dna_similarity"] = dna_sim

            # Temporal proximity scoring
            dt = abs((inc1.created_at - inc2.created_at).total_seconds()) / 3600.0
            if dt <= 24:
                temporal_score = max(0.0, 1.0 - (dt / 24.0))
                ml_prob += temporal_score * 0.30
                feature_contributions["temporal_proximity_24h"] = round(temporal_score, 4)

        relationship_probability = round(min(max(ml_prob, 0.0), 1.0), 4)

        # ── 2. Deterministic Corroboration & Verification ──────────────────
        evidence_chain: List[Evidence] = []
        rel_type = RelationshipType.SIMILAR_DNA
        deterministic_weight = 0.0

        # Exact infrastructure matches
        shared_phones = set()
        shared_upis = set()
        shared_urls = set()

        if inc1.scam_dna and inc2.scam_dna:
            shared_phones = set(inc1.scam_dna.phone_numbers).intersection(set(inc2.scam_dna.phone_numbers))
            shared_upis = set(inc1.scam_dna.upi_ids).intersection(set(inc2.scam_dna.upi_ids))
            shared_urls = set(inc1.scam_dna.urls).intersection(set(inc2.scam_dna.urls))

        if shared_upis:
            rel_type = RelationshipType.SHARED_UPI
            deterministic_weight += 0.50
            evidence_chain.append(
                Evidence(
                    claim=f"Shared UPI ID observed: {list(shared_upis)[0]}",
                    type=ProvenanceType.OBSERVED,
                    source="entity_resolver",
                    evidence_confidence=0.98,
                    supporting_incident_ids=[inc1.id, inc2.id],
                    scoring_factors={"shared_upi_match": 0.50},
                )
            )

        if shared_phones:
            rel_type = RelationshipType.SHARED_PHONE
            deterministic_weight += 0.45
            evidence_chain.append(
                Evidence(
                    claim=f"Shared phone number observed: {list(shared_phones)[0]}",
                    type=ProvenanceType.OBSERVED,
                    source="entity_resolver",
                    evidence_confidence=0.95,
                    supporting_incident_ids=[inc1.id, inc2.id],
                    scoring_factors={"shared_phone_match": 0.45},
                )
            )

        if shared_urls:
            rel_type = RelationshipType.SHARED_URL
            deterministic_weight += 0.40
            evidence_chain.append(
                Evidence(
                    claim=f"Shared URL observed: {list(shared_urls)[0]}",
                    type=ProvenanceType.OBSERVED,
                    source="entity_resolver",
                    evidence_confidence=0.92,
                    supporting_incident_ids=[inc1.id, inc2.id],
                    scoring_factors={"shared_url_match": 0.40},
                )
            )

        # Inferred ScamDNA similarity evidence
        if dna_sim >= 0.75:
            evidence_chain.append(
                Evidence(
                    claim=f"High behavioral ScamDNA similarity ({dna_sim:.2f})",
                    type=ProvenanceType.INFERRED,
                    source="similarity_service",
                    evidence_confidence=dna_sim,
                    supporting_incident_ids=[inc1.id, inc2.id],
                    scoring_factors={"dna_similarity": dna_sim},
                )
            )

        # ── 3. Rule Enforcement: ML alone cannot produce high confidence ──
        # If there is NO deterministic evidence, relationship_confidence is capped at 0.40
        if not evidence_chain or all(e.type != ProvenanceType.OBSERVED for e in evidence_chain):
            relationship_confidence = round(min(relationship_probability * 0.40, 0.40), 4)
            is_verified = False
        else:
            relationship_confidence = round(min(0.30 * relationship_probability + deterministic_weight, 1.0), 4)
            is_verified = relationship_confidence >= 0.60

        # Don't emit empty or negligible relationships
        if relationship_probability < 0.20 and relationship_confidence < 0.20:
            return None

        explanation_lines = [f"ML Likelihood Score: {relationship_probability:.2f}", f"Verified Confidence: {relationship_confidence:.2f}"]
        if is_verified:
            explanation_lines.append("Verified by deterministic infrastructure match.")
        else:
            explanation_lines.append("Unverified candidate: insufficient deterministic corroboration.")

        return Relationship(
            source_incident_id=inc1.id,
            target_incident_id=inc2.id,
            relationship_type=rel_type,
            relationship_probability=relationship_probability,
            relationship_confidence=relationship_confidence,
            supporting_evidence=evidence_chain,
            feature_contributions=feature_contributions,
            explanation=" ".join(explanation_lines),
            is_verified=is_verified,
        )
