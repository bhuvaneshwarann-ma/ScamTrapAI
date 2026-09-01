"""
ScamTrap AI — Trojan Victim Protocol & Threat Playbook Models

Data models for:
1. Trojan Victim Protocol (Honey-tokens, Beacon files, Syndicate IP & Supply Chain tracking)
2. Reverse-Engineered Threat Playbook (SOP Manual, Objection Handling, Escalation Hierarchy)
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TrojanVictimProfile(BaseModel):
    """Synthetic Trojan Victim persona with embedded honey-tokens."""
    profile_id: str
    target_campaign_id: str
    persona_name: str
    synthetic_phone: str
    synthetic_email: str
    beacon_file_name: str = "Bank_Statement_Final.pdf"
    tracking_beacon_url: str
    beacon_status: str = "armed"  # armed | pinged | logged_to_crm | dark_web_resold
    syndicate_ip: Optional[str] = None
    syndicate_device_fingerprint: Optional[str] = None
    syndicate_tier: str = "Tier 1 (Call Center Operator)"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StressTestReaction(BaseModel):
    """Adversarial stress test reaction metadata."""
    test_type: str  # authority | technical | financial
    stress_prompt: str
    scammer_reaction: str
    escalated_to_supervisor: bool = False
    syndicate_sophistication_score: float = Field(ge=0.0, le=1.0)


class ThreatPlaybook(BaseModel):
    """Reverse-engineered Standard Operating Procedure (SOP) Playbook."""
    playbook_id: str
    campaign_id: str
    target_impersonation: str
    the_hook: str
    objection_handling_matrix: Dict[str, str]
    psychological_pressure_points: List[str]
    escalation_pathway: List[str]
    recommended_bank_chatbot_defenses: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
