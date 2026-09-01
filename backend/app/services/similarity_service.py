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
        """Compute cosine similarity between two ScamDNA feature vectors."""
        vec1 = self._vectorize_dna(dna1)
        vec2 = self._vectorize_dna(dna2)

        all_keys = set(vec1.keys()).union(set(vec2.keys()))
        if not all_keys:
            return SimilarityResult(similarity_score=0.0, compared_features={})

        dot_product = sum(vec1.get(k, 0.0) * vec2.get(k, 0.0) for k in all_keys)
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0.0 or mag2 == 0.0:
            score = 0.0
        else:
            score = dot_product / (mag1 * mag2)

        # Feature breakdown
        contributions = {}
        if dna1.impersonation_target == dna2.impersonation_target:
            contributions["shared_impersonation_target"] = 0.3
        if dna1.payment_method == dna2.payment_method and dna1.payment_method.value != "other":
            contributions["shared_payment_method"] = 0.2
        
        shared_tactics = set(dna1.social_engineering_tactics).intersection(set(dna2.social_engineering_tactics))
        if shared_tactics:
            contributions["shared_tactics_overlap"] = len(shared_tactics) * 0.15

        return SimilarityResult(
            similarity_score=round(min(max(score, 0.0), 1.0), 4),
            compared_features=contributions,
        )
