"""
ScamTrap AI — Trojan Victim Protocol & Threat Playbooks API Router

Endpoints:
- POST /api/v1/trojan-victim/generate
- POST /api/v1/trojan-victim/stress-test
- GET /api/v1/playbooks/{campaign_id}
"""

from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.trojan_victim_service import TrojanVictimService

router = APIRouter(prefix="/api/v1", tags=["trojan-victim"])
service = TrojanVictimService()


class GenerateTrojanRequest(BaseModel):
    campaign_id: str = "CAMP-01-SBI-KYC"
    impersonation: str = "bank"


class StressTestRequest(BaseModel):
    test_type: str = "authority"  # authority | technical | financial


@router.post("/trojan-victim/generate")
async def generate_trojan_profile(req: GenerateTrojanRequest) -> Dict[str, Any]:
    """Mint Trojan Victim profile with embedded honey-token beacon."""
    profile = service.generate_trojan_profile(req.campaign_id, req.impersonation)
    return profile.model_dump(mode="json")


@router.post("/trojan-victim/stress-test")
async def run_stress_test(req: StressTestRequest) -> Dict[str, Any]:
    """Inject adversarial conversational stress test to map syndicate hierarchy."""
    res = service.run_adversarial_stress_test(req.test_type)
    return res.model_dump(mode="json")


@router.get("/playbooks/{campaign_id}")
async def get_threat_playbook(campaign_id: str) -> Dict[str, Any]:
    """Reverse-engineer Standard Operating Procedure (SOP) Threat Playbook for a campaign."""
    playbook = service.reverse_engineer_playbook(campaign_id, "bank")
    return playbook.model_dump(mode="json")
