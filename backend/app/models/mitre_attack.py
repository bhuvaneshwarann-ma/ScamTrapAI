"""
ScamTrap AI — MITRE ATT&CK & CTI Models

Data models for:
1. MITRE ATT&CK Technique Mapping & Matrix
2. Unified IOC Search Results
3. Real-Time CTI Threat Feed Items
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class MitreTechnique(BaseModel):
    """MITRE ATT&CK Technique Model."""
    technique_id: str  # e.g., T1566.002
    name: str
    tactic: str  # Initial Access | Reconnaissance | Credential Access | Impact
    description: str
    observed_count: int = 1
    confidence: float = 0.95


class MitreMatrixResponse(BaseModel):
    """Full MITRE ATT&CK Heatmap Matrix payload."""
    tactics: Dict[str, List[MitreTechnique]]
    total_techniques_detected: int
    most_frequent_technique: str


class IOCSearchResult(BaseModel):
    """Unified IOC Search Result object."""
    ioc_value: str
    ioc_type: str  # phone | upi | url | domain | ip | hash | email
    threat_score: int = Field(ge=0, le=100)
    verdict: str  # MALICIOUS | SUSPICIOUS | BENIGN
    first_seen: str
    last_seen: str
    associated_campaign_ids: List[str]
    mitre_techniques: List[str]
    enrichment_sources: List[str]


class ThreatFeedItem(BaseModel):
    """Real-Time CTI Threat Feed Record."""
    feed_id: str
    title: str
    source: str  # OSINT | DarkWeb | Cert-In | PhishTank
    indicator: str
    threat_level: str  # CRITICAL | HIGH | MEDIUM | LOW
    description: str
    timestamp: str
