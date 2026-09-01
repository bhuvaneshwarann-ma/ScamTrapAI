"""
ScamTrap AI — Evidence & Explainability Engine (Phase 10)

Queries and populates canonical Evidence objects to answer "why are these incidents connected?".

Preserves strict provenance (§3.2, Phase 10):
- OBSERVED: Direct ground truth (shared UPI, phone, domain)
- INFERRED: Heuristic / ScamDNA similarity
- PREDICTED: Statistical ML similarity score

Rules:
- Never convert inferred information into observed facts.
- Never claim criminal identity or legal guilt.
- Preserve uncertainty explicitly.
"""

from typing import List, Dict, Any
from backend.app.models.enums import ProvenanceType
from backend.app.models.evidence import Evidence
from backend.app.models.relationship import Relationship


class EvidenceService:
    """Explainability & Evidence Query Engine."""

    def explain_relationship(self, relationship: Relationship) -> Dict[str, Any]:
        """
        Generate structured, evidence-bounded explanation of a relationship
        with strict provenance separation.
        """
        observed_facts = [e for e in relationship.supporting_evidence if e.type == ProvenanceType.OBSERVED]
        inferred_facts = [e for e in relationship.supporting_evidence if e.type == ProvenanceType.INFERRED]
        predicted_facts = [e for e in relationship.supporting_evidence if e.type == ProvenanceType.PREDICTED]

        return {
            "relationship_id": relationship.id,
            "relationship_type": relationship.relationship_type.value if hasattr(relationship.relationship_type, "value") else str(relationship.relationship_type),
            "relationship_confidence": relationship.relationship_confidence,  # Investigator-facing
            "relationship_probability": relationship.relationship_probability,  # Internal ML score
            "is_verified": relationship.is_verified,
            "provenance_breakdown": {
                "observed": [e.claim for e in observed_facts],
                "inferred": [e.claim for e in inferred_facts],
                "predicted": [e.claim for e in predicted_facts],
            },
            "evidence_count": len(relationship.supporting_evidence),
            "explanation": relationship.explanation,
            "disclaimer": "DISCLAIMER: EVIDENCE-BOUNDED ASSESSMENT -- SYNTHETIC DEMO ENVIRONMENT. DOES NOT CONSTITUTE LEGAL ACCUSATION OR CRIMINAL ATTRIBUTION."
        }
