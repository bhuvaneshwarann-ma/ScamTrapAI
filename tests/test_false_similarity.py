"""
ScamTrap AI — False Similarity Test Suite (Master Prompt #11 & #22)

Validates:
- Incidents A, B, C (English, Tamil, Hindi SBI KYC scams with shared phone/UPI/URL) form a Campaign.
- Incident D (Legitimate SBI notification containing words 'SBI', 'bank', 'account', 'KYC' but NO shared infrastructure) is REJECTED and stays OUTSIDE the campaign cluster.
"""

import pytest
from backend.app.models.enums import IncidentChannel
from backend.app.models.incident import Incident
from backend.app.services.llm_provider import MockLLMProvider
from backend.app.services.relationship_engine import RelationshipEngine
from backend.app.services.campaign_detector import CampaignDetector


@pytest.mark.asyncio
async def test_false_similarity_rejection_scenario():
    llm = MockLLMProvider()
    engine = RelationshipEngine()
    detector = CampaignDetector(min_incidents=2, min_relationship_confidence=0.60)

    # Incident A — English SBI KYC Scam
    text_a = "SBI ALERT: Your account suspended due to KYC update. Visit https://sbi-kyc-update-portal.xyz/verify or pay Rs 1 to sbi.kyc.update@ybl. Call +919876543210."
    dna_a = await llm.extract_scam_dna(text_a, IncidentChannel.SMS)
    inc_a = Incident(id="inc-a", raw_text=text_a, channel=IncidentChannel.SMS, scam_dna=dna_a, ground_truth_campaign_id="CAMP-SBI-KYC-01")

    # Incident B — Tamil SBI KYC Scam
    text_b = "வணக்கம், உங்கள் SBI கணக்கு முடக்கப்படும். உடனடியாக KYC புதுப்பிக்கவும்: https://sbi-kyc-update-portal.xyz/verify. UPI: sbi.kyc.update@ybl. தொடர்புக்கு: +919876543210."
    dna_b = await llm.extract_scam_dna(text_b, IncidentChannel.WHATSAPP)
    inc_b = Incident(id="inc-b", raw_text=text_b, channel=IncidentChannel.WHATSAPP, scam_dna=dna_b, ground_truth_campaign_id="CAMP-SBI-KYC-01")

    # Incident C — Hindi SBI KYC Scam
    text_c = "प्रिय ग्राहक, आपका SBI बैंक खाता ब्लॉक हो गया है। तुरंत KYC अपडेट करें https://sbi-kyc-update-portal.xyz/verify या UPI sbi.kyc.update@ybl। कॉल +919876543210।"
    dna_c = await llm.extract_scam_dna(text_c, IncidentChannel.SMS)
    inc_c = Incident(id="inc-c", raw_text=text_c, channel=IncidentChannel.SMS, scam_dna=dna_c, ground_truth_campaign_id="CAMP-SBI-KYC-01")

    # Incident D — Legitimate SBI Notification (FALSE SIMILARITY CONTROL)
    text_d = "Dear customer, your monthly SBI bank statement for August is ready. View it safely in your YONO app. SBI will never ask for your OTP or password."
    dna_d = await llm.extract_scam_dna(text_d, IncidentChannel.SMS)
    inc_d = Incident(id="inc-d", raw_text=text_d, channel=IncidentChannel.SMS, scam_dna=dna_d, ground_truth_campaign_id="CAMP-LEGIT-SBI-99")

    incidents = [inc_a, inc_b, inc_c, inc_d]

    # Evaluate all pairs
    relationships = []
    for i in range(len(incidents)):
        for j in range(i + 1, len(incidents)):
            rel = engine.evaluate_pair(incidents[i], incidents[j])
            if rel:
                relationships.append(rel)

    # Detect campaigns
    detected = detector.detect_campaigns(incidents, relationships)

    assert len(detected) == 1, "Incidents A, B, C should form exactly 1 campaign"
    camp, alert = detected[0]

    # Verify A, B, C are inside campaign
    assert "inc-a" in camp.incident_ids
    assert "inc-b" in camp.incident_ids
    assert "inc-c" in camp.incident_ids

    # HARD RULE: Incident D MUST NOT be inside campaign!
    assert "inc-d" not in camp.incident_ids, "Incident D (False Similarity) MUST be rejected from campaign cluster!"
