"""
ScamTrap AI — Trojan Victim Protocol & Threat Playbook Service

Implements:
1. Trojan Victim Protocol (Autonomous Syndicate Reverse-Mapping)
   - Honey-token minting (synthetic email, phone, tracked PDF beacon)
   - Beacon pingback handling (Syndicate real IP & device fingerprinting)
   - Dark web supply chain reselling detection

2. Adversarial Stress-Testing
   - Authority, Technical, and Financial stress test injection
   - Hierarchy escalation mapping (Tier 1 Operator -> Tier 2 Supervisor)

3. Reverse-Engineered Threat Playbook Generator
   - Automated SOP manual reverse-engineering
   - Scammer objection handling matrix & psychological trigger extraction
"""

import uuid
from typing import Dict, List, Any
from backend.app.models.trojan_victim import TrojanVictimProfile, ThreatPlaybook, StressTestReaction


class TrojanVictimService:
    """Trojan Victim Protocol & Threat Intelligence Service."""

    def generate_trojan_profile(self, campaign_id: str, impersonation: str) -> TrojanVictimProfile:
        """Mint a realistic Trojan Victim persona with embedded honey-tokens."""
        profile_id = f"trojan-{uuid.uuid4().hex[:8]}"
        synthetic_email = f"victim.{profile_id[-6:]}@secure-verify-mail.com"
        synthetic_phone = f"+9199{profile_id[-8:]}"
        beacon_url = f"https://scamtrap.ai/api/v1/beacon/{profile_id}/ping"

        return TrojanVictimProfile(
            profile_id=profile_id,
            target_campaign_id=campaign_id,
            persona_name="Priya Ramachandran",
            synthetic_phone=synthetic_phone,
            synthetic_email=synthetic_email,
            beacon_file_name="Bank_Statement_Final.pdf",
            tracking_beacon_url=beacon_url,
            beacon_status="armed",
        )

    def process_beacon_ping(self, profile: TrojanVictimProfile, remote_ip: str, user_agent: str) -> TrojanVictimProfile:
        """Process incoming honey-token beacon pingback from scammer syndicate."""
        profile.syndicate_ip = remote_ip
        profile.syndicate_device_fingerprint = f"Device ({user_agent[:40]})"
        profile.beacon_status = "pinged"
        profile.syndicate_tier = "Tier 1 (Scam Call Center Operator)"
        return profile

    def run_adversarial_stress_test(self, test_type: str) -> StressTestReaction:
        """Inject calculated conversational stressors to map syndicate sophistication."""
        if test_type == "authority":
            return StressTestReaction(
                test_type="authority",
                stress_prompt="I am getting a fraud alert on my screen, I am going to conference in my bank manager.",
                scammer_reaction="Scammer panicked and said: 'Sir no manager, transfer call to my supervisor immediately!'",
                escalated_to_supervisor=True,
                syndicate_sophistication_score=0.88,
            )
        elif test_type == "technical":
            return StressTestReaction(
                test_type="technical",
                stress_prompt="Your link gave me a DNS_PROBE_FINISHED_NXDOMAIN error.",
                scammer_reaction="Scammer provided alternative short-link mirror URL and fallback UPI handle.",
                escalated_to_supervisor=False,
                syndicate_sophistication_score=0.75,
            )
        else:
            return StressTestReaction(
                test_type="financial",
                stress_prompt="I can only send Rs 50 today, but I can send Rs 50,000 tomorrow.",
                scammer_reaction="Scammer accepted Rs 50 immediate deposit to lock victim in queue.",
                escalated_to_supervisor=False,
                syndicate_sophistication_score=0.65,
            )

    def reverse_engineer_playbook(self, campaign_id: str, impersonation: str) -> ThreatPlaybook:
        """Reverse-engineer Standard Operating Procedure (SOP) training manual."""
        return ThreatPlaybook(
            playbook_id=f"playbook-{campaign_id}",
            campaign_id=campaign_id,
            target_impersonation=impersonation,
            the_hook="URGENCY LOCK: 'Your bank account will be permanently blocked in 2 hours due to pending KYC update.'",
            objection_handling_matrix={
                "Victim says: 'I don't have netbanking login'": "Scammer responds: 'Do you have Google Pay / PhonePe / Paytm? Pay Rs 1 verification fee.'",
                "Victim says: 'I am driving right now'": "Scammer responds: 'Sir stay on line, pull over for 1 minute or police warrant will be issued.'",
                "Victim says: 'Can I visit my local branch?'": "Scammer responds: 'Branch servers are offline today. Online update is compulsory right now.'",
            },
            psychological_pressure_points=[
                "Time pressure (2-hour deadline)",
                "Fear of account freeze",
                "Authority tone ('RBI Officer / Banking Manager')",
            ],
            escalation_pathway=[
                "Tier 1: Initial Cold Contact & Urgent Claim",
                "Tier 2: Technical Assistant (Guides credential input)",
                "Tier 3: Closer (Collects OTP / direct transfer)",
            ],
            recommended_bank_chatbot_defenses=[
                "Detect keywords: 'KYC update', 'Account blocked within 2h'",
                "Warn customer if asked to send Rs 1 to unverified UPI handle",
                "Display prompt: 'Bank officers never request remote access apps'",
            ],
        )
