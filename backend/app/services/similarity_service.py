"""
ScamTrap AI — Semantic Embedding & ML Similarity Service (Phase 6)

Embeds structured ScamDNA + normalized behavioral features (tactics, target,
script traits), rather than relying only on surface keywords.

Provides:
- Feature vectorization from ScamDNA
- Cosine similarity computation
- Similarity result payload with feature breakdown, model version, and timestamp
- Offline fallback mock vectorizer
"""

import math
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from pydantic import BaseModel, Field

from backend.app.models.scam_dna import ScamDNA


class SimilarityResult(BaseModel):
    """Output payload for pairwise ScamDNA behavioral similarity."""
    similarity_score: float = Field(ge=0.0, le=1.0)
    entity_overlap_score: float = Field(default=0.0, ge=0.0, le=1.0)
    tactic_similarity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    semantic_similarity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    urgency_similarity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    primary_evidence_reasons: List[str] = Field(default_factory=list)
    compared_features: Dict[str, float] = Field(default_factory=dict)
    model_version: str = "behavioral-feature-v1.0"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SimilarityService:
    """Computes behavioral vector similarity between ScamDNA objects."""

    @staticmethod
    def _vectorize_dna(dna: ScamDNA) -> Dict[str, float]:
        """Convert ScamDNA into a normalized behavioral feature vector."""
        vec: Dict[str, float] = {}

        # Impersonation target feature
        vec[f"target_{dna.impersonation_target.value}"] = 1.0

        # Payment method feature
        vec[f"payment_{dna.payment_method.value}"] = 1.0

        # Behavioral pressure levels
        vec["urgency"] = dna.urgency
        vec["fear"] = dna.fear
        vec["authority_pressure"] = dna.authority_pressure
        vec["credential_request"] = 1.0 if dna.credential_request else 0.0
        vec["payment_request"] = 1.0 if dna.payment_request else 0.0

        # Social engineering tactics
        for tactic in dna.social_engineering_tactics:
            vec[f"tactic_{tactic.value}"] = 1.0

        return vec

    def compute_similarity(self, dna1: ScamDNA, dna2: ScamDNA) -> SimilarityResult:
        """Compute cosine similarity between two ScamDNA feature vectors with explicit evidence breakdown."""
        vec1 = self._vectorize_dna(dna1)
        vec2 = self._vectorize_dna(dna2)

        all_keys = set(vec1.keys()).union(set(vec2.keys()))
        if not all_keys:
            return SimilarityResult(
                similarity_score=0.0,
                entity_overlap_score=0.0,
                tactic_similarity_score=0.0,
                semantic_similarity_score=0.0,
                urgency_similarity_score=0.0,
                primary_evidence_reasons=[],
                compared_features={},
            )

        dot_product = sum(vec1.get(k, 0.0) * vec2.get(k, 0.0) for k in all_keys)
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        score = dot_product / (mag1 * mag2) if (mag1 > 0 and mag2 > 0) else 0.0

        # Sub-score calculations
        # 1. Entity Overlap
        entities1 = set(dna1.phone_numbers + dna1.upi_ids + dna1.urls + dna1.domains + dna1.emails)
        entities2 = set(dna2.phone_numbers + dna2.upi_ids + dna2.urls + dna2.domains + dna2.emails)
        if entities1 and entities2:
            entity_overlap = len(entities1.intersection(entities2)) / len(entities1.union(entities2))
        else:
            entity_overlap = 0.0

        # 2. Tactic Jaccard Similarity
        tactics1 = set(dna1.social_engineering_tactics)
        tactics2 = set(dna2.social_engineering_tactics)
        if tactics1 and tactics2:
            tactic_sim = len(tactics1.intersection(tactics2)) / len(tactics1.union(tactics2))
        else:
            tactic_sim = 1.0 if not tactics1 and not tactics2 else 0.0

        # 3. Urgency Similarity
        urgency_sim = max(0.0, 1.0 - abs(dna1.urgency - dna2.urgency))

        # Primary evidence reasons
        evidence_reasons: List[str] = []
        if entities1.intersection(entities2):
            evidence_reasons.append(f"Shared infrastructure indicators ({', '.join(list(entities1.intersection(entities2))[:3])})")
        if dna1.impersonation_target == dna2.impersonation_target:
            evidence_reasons.append(f"Identical impersonation target ({dna1.impersonation_target.value})")
        if tactics1.intersection(tactics2):
            evidence_reasons.append(f"Shared psychological tactics ({', '.join([t.value for t in tactics1.intersection(tactics2)])})")
        if dna1.payment_method == dna2.payment_method and dna1.payment_method.value != "other":
            evidence_reasons.append(f"Matching payment method ({dna1.payment_method.value})")

        contributions = {}
        if dna1.impersonation_target == dna2.impersonation_target:
            contributions["shared_impersonation_target"] = 0.3
        if dna1.payment_method == dna2.payment_method and dna1.payment_method.value != "other":
            contributions["shared_payment_method"] = 0.2
        if tactics1.intersection(tactics2):
            contributions["shared_tactics_overlap"] = len(tactics1.intersection(tactics2)) * 0.15

        final_score = round(min(max(score, 0.0), 1.0), 4)

        return SimilarityResult(
            similarity_score=final_score,
            entity_overlap_score=round(entity_overlap, 4),
            tactic_similarity_score=round(tactic_sim, 4),
            semantic_similarity_score=final_score,
            urgency_similarity_score=round(urgency_sim, 4),
            primary_evidence_reasons=evidence_reasons,
            compared_features=contributions,
        )
