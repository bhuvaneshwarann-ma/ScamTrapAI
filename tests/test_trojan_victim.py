"""
ScamTrap AI — Trojan Victim & Playbook Service Tests

Validates:
- Trojan Victim profile generation and honey-token URL minting
- Adversarial stress testing (authority, technical, financial)
- Reverse-engineered Threat Playbook (SOP manual) generation
"""

import pytest
from backend.app.services.trojan_victim_service import TrojanVictimService


def test_trojan_profile_generation():
    service = TrojanVictimService()
    profile = service.generate_trojan_profile("CAMP-01-SBI-KYC", "bank")

    assert profile.profile_id.startswith("trojan-")
    assert profile.target_campaign_id == "CAMP-01-SBI-KYC"
    assert "ping" in profile.tracking_beacon_url
    assert profile.beacon_file_name == "Bank_Statement_Final.pdf"


def test_adversarial_stress_test():
    service = TrojanVictimService()
    res_auth = service.run_adversarial_stress_test("authority")
    assert res_auth.escalated_to_supervisor is True
    assert res_auth.syndicate_sophistication_score >= 0.80

    res_tech = service.run_adversarial_stress_test("technical")
    assert res_tech.escalated_to_supervisor is False


def test_reverse_engineer_playbook():
    service = TrojanVictimService()
    playbook = service.reverse_engineer_playbook("CAMP-01-SBI-KYC", "bank")

    assert playbook.campaign_id == "CAMP-01-SBI-KYC"
    assert len(playbook.objection_handling_matrix) >= 2
    assert len(playbook.recommended_bank_chatbot_defenses) >= 2
