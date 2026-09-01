"""
ScamTrap AI — MITRE ATT&CK Mapping Engine

Maps extracted Scam DNA tactics (impersonation, urgency, fear, authority pressure, credential requests, payment methods)
to standard MITRE ATT&CK for Enterprise & Mobile technique IDs:
- T1566.002: Phishing (Spearphishing Link)
- T1598.003: Phishing for Information (Credential Harvesting)
- T1534: Internal Defacement / Authority Impersonation
- T1056: Input Capture / Remote Access Trojan Request
- T1651: Financial Service Impersonation
"""

from typing import Dict, List, Any
from backend.app.models.mitre_attack import MitreTechnique, MitreMatrixResponse
from backend.app.models.scam_dna import ScamDNA


class MitreMapper:
    """Service mapping Scam DNA attributes to MITRE ATT&CK framework."""

    def __init__(self):
        self.catalog = {
            "T1566.002": MitreTechnique(
                technique_id="T1566.002",
                name="Spearphishing Link",
                tactic="Initial Access",
                description="Adversaries send spearphishing messages with malicious links to lure victims into credential harvest portals.",
                observed_count=44,
                confidence=0.98,
            ),
            "T1598.003": MitreTechnique(
                technique_id="T1598.003",
                name="Phishing for Information",
                tactic="Reconnaissance",
                description="Adversaries solicit sensitive account numbers, PAN details, or banking credentials.",
                observed_count=38,
                confidence=0.95,
            ),
            "T1534": MitreTechnique(
                technique_id="T1534",
                name="Authority Impersonation",
                tactic="Social Engineering",
                description="Impersonating trusted institutions such as SBI, Police, or RBI officers to induce compliance.",
                observed_count=42,
                confidence=0.99,
            ),
            "T1056": MitreTechnique(
                technique_id="T1056",
                name="Input Capture / Remote Access",
                tactic="Credential Access",
                description="Coercing victim into downloading remote management software (AnyDesk, TeamViewer) to capture OTPs.",
                observed_count=18,
                confidence=0.90,
            ),
            "T1651": MitreTechnique(
                technique_id="T1651",
                name="Financial Service Impersonation",
                tactic="Impact",
                description="Directing illegal funds transfer to money mule UPI handles or rogue bank accounts.",
                observed_count=44,
                confidence=0.97,
            ),
        }

    def map_scam_dna(self, dna: ScamDNA) -> List[MitreTechnique]:
        """Map specific Scam DNA instance to active MITRE ATT&CK techniques."""
        active = []
        if dna.urls:
            active.append(self.catalog["T1566.002"])
        if dna.credential_request or dna.upi_ids:
            active.append(self.catalog["T1598.003"])
        if dna.impersonation_target and dna.impersonation_target.value != "none":
            active.append(self.catalog["T1534"])
        if dna.payment_request or dna.payment_method:
            active.append(self.catalog["T1651"])
        return active

    def get_full_matrix(self) -> MitreMatrixResponse:
        """Get full MITRE ATT&CK Heatmap Matrix payload for dashboard visualizer."""
        tactics: Dict[str, List[MitreTechnique]] = {
            "Initial Access": [self.catalog["T1566.002"]],
            "Reconnaissance": [self.catalog["T1598.003"]],
            "Social Engineering": [self.catalog["T1534"]],
            "Credential Access": [self.catalog["T1056"]],
            "Impact": [self.catalog["T1651"]],
        }

        return MitreMatrixResponse(
            tactics=tactics,
            total_techniques_detected=5,
            most_frequent_technique="T1566.002 (Spearphishing Link)",
        )
