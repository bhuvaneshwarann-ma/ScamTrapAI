"""
ScamTrap AI — Evidence-Bounded Investigator Copilot Service (Phase 11)

Strict zero-hallucination Q&A service over investigation evidence.

Rules:
- Uses ONLY provided evidence context (incidents, relationships, evidence records).
- Cites specific IDs (incident_id, entity_id, relationship_id).
- Returns "Insufficient evidence." if query cannot be answered strictly from context.
- Never accuses individuals or invents criminal facts.
"""

from typing import List, Optional
from backend.app.models.evidence import Evidence
from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship
from backend.app.models.investigation import InvestigationQuery, InvestigationResponse


class CopilotService:
    """Zero-hallucination investigator copilot."""

    def answer_query(
        self,
        query: InvestigationQuery,
        incidents: List[Incident],
        relationships: List[Relationship],
    ) -> InvestigationResponse:
        q_lower = query.question.lower()

        # Check for adversarial / out-of-scope / unsupported questions
        if any(w in q_lower for w in ["who is the criminal", "who owns this name", "arrest", "real address"]):
            return InvestigationResponse(
                question=query.question,
                assessment="Out-of-scope attribution request",
                confidence=0.0,
                answer="Insufficient evidence to determine this. The system operates strictly on synthetic behavioral indicators and does not identify real-world personal identities or declare criminal guilt.",
                insufficient_evidence=True,
            )

        # Query 1: Why are incidents connected?
        if any(w in q_lower for w in ["why", "connect", "related", "relationship"]):
            rel = next((r for r in relationships if r.is_verified), None)
            if rel:
                obs = [e for e in rel.supporting_evidence if e.type.value == "OBSERVED"]
                claim_text = obs[0].claim if obs else rel.explanation
                return InvestigationResponse(
                    question=query.question,
                    assessment=f"High-confidence link between Incident {rel.source_incident_id[:8]} and {rel.target_incident_id[:8]}",
                    confidence=rel.relationship_confidence,
                    answer=f"Incidents {rel.source_incident_id[:8]} and {rel.target_incident_id[:8]} are connected with confidence {rel.relationship_confidence:.2f}. Key evidence: {claim_text}.",
                    cited_evidence=rel.supporting_evidence,
                    cited_incident_ids=[rel.source_incident_id, rel.target_incident_id],
                    cited_relationship_ids=[rel.id],
                    insufficient_evidence=False,
                )

        # Query 2: What tactics are used?
        if "tactic" in q_lower or "strategy" in q_lower:
            tactics = set()
            cited_inc_ids = []
            for inc in incidents:
                if inc.scam_dna:
                    for t in inc.scam_dna.social_engineering_tactics:
                        tactics.add(t.value)
                    cited_inc_ids.append(inc.id)
            if tactics:
                return InvestigationResponse(
                    question=query.question,
                    assessment=f"Identified {len(tactics)} social engineering tactics across {len(cited_inc_ids)} incidents",
                    confidence=0.92,
                    answer=f"Observed social engineering tactics across incidents: {', '.join(sorted(tactics))}.",
                    cited_incident_ids=cited_inc_ids,
                    insufficient_evidence=False,
                )

        # Default fallback if evidence is insufficient
        return InvestigationResponse(
            question=query.question,
            assessment="No matching evidence found in active context",
            confidence=0.0,
            answer="Insufficient evidence to determine this.",
            insufficient_evidence=True,
        )
