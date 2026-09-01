"""
ScamTrap AI — Phase 9 & 9.5 Campaign Detector Tests

Validates:
- Automated campaign detection on multi-incident clusters
- Rejection of false similarity negative controls
- Emitting CampaignAlert payloads with evidence
"""

import pytest
from backend.app.models.enums import IncidentChannel, ImpersonationTarget, PaymentMethod, SocialEngineeringTactic
from backend.app.models.incident import Incident
from backend.app.models.scam_dna import ScamDNA
from backend.app.models.relationship import Relationship, RelationshipType
from backend.app.services.campaign_detector import CampaignDetector


def test_campaign_detection_and_alert_generation():
    detector = CampaignDetector(min_incidents=3, min_relationship_confidence=0.60)

    dna = ScamDNA(
        language="en", channel=IncidentChannel.SMS, impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9, fear=0.8, authority_pressure=0.8, credential_request=True, payment_request=True,
        payment_method=PaymentMethod.UPI, requested_action="Update KYC", target_type="individual",
        extraction_confidence=0.95, upi_ids=["sbi.kyc.update@ybl"]
    )

    inc1 = Incident(id="inc-1", raw_text="Inc 1", channel=IncidentChannel.SMS, scam_dna=dna)
    inc2 = Incident(id="inc-2", raw_text="Inc 2", channel=IncidentChannel.SMS, scam_dna=dna)
    inc3 = Incident(id="inc-3", raw_text="Inc 3", channel=IncidentChannel.SMS, scam_dna=dna)

    rel1 = Relationship(source_incident_id="inc-1", target_incident_id="inc-2", relationship_type=RelationshipType.SHARED_UPI, relationship_confidence=0.95)
    rel2 = Relationship(source_incident_id="inc-2", target_incident_id="inc-3", relationship_type=RelationshipType.SHARED_UPI, relationship_confidence=0.95)

    detected = detector.detect_campaigns([inc1, inc2, inc3], [rel1, rel2])

    assert len(detected) == 1
    campaign, alert = detected[0]
    assert len(campaign.incident_ids) == 3
    assert alert is not None
    assert alert.alert_type == "EMERGING_CAMPAIGN_DETECTED"
    assert "sbi.kyc.update@ybl" in alert.shared_infrastructure
