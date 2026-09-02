"""
ScamTrap AI — Campaign Detection & Early Warning Service (Phase 9 & 9.5)

Detects emerging scam campaigns by clustering incidents linked by verified
relationships and shared infrastructure.

Configurable detection thresholds calibrated in Phase 9.5:
- `min_incidents` (default 3)
- `min_relationship_confidence` (default 0.60)
"""

from typing import List, Optional, Dict, Set, Tuple
from datetime import datetime, timezone

from backend.app.models.enums import CampaignStatus, RiskLevel
from backend.app.models.campaign import Campaign, CampaignAlert, TimelineItem
from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship
from backend.app.services.graph_engine import GraphEngine


class CampaignDetector:
    """Detects campaigns and emits UI-ready alert payloads."""

    def __init__(self, min_incidents: int = 3, min_relationship_confidence: float = 0.60):
        self.min_incidents = min_incidents
        self.min_relationship_confidence = min_relationship_confidence
        self.graph_engine = GraphEngine()

    def detect_campaigns(self, incidents: List[Incident], relationships: List[Relationship]) -> List[Tuple[Campaign, Optional[CampaignAlert]]]:
        """
        Analyze incidents and relationships, returning detected campaigns
        and alert payloads when emerging campaigns pass detection thresholds.
        """
        # Filter for verified or sufficiently high-confidence relationships
        valid_rels = [r for r in relationships if r.relationship_confidence >= self.min_relationship_confidence]
        
        # Build graph
        self.graph_engine.build_graph(incidents, valid_rels)

        clusters = self.graph_engine.get_clusters()
        inc_map = {inc.id: inc for inc in incidents}

        results = []
        for cluster_ids in clusters:
            if len(cluster_ids) < self.min_incidents:
                continue

            cluster_incidents = [inc_map[i_id] for i_id in cluster_ids if i_id in inc_map]
            
            # Aggregate shared infrastructure and tactics
            shared_phones = set()
            shared_upis = set()
            shared_urls = set()
            shared_tactics = set()

            for inc in cluster_incidents:
                if inc.scam_dna:
                    shared_phones.update(inc.scam_dna.phone_numbers)
                    shared_upis.update(inc.scam_dna.upi_ids)
                    shared_urls.update(inc.scam_dna.urls)
                    shared_tactics.update([t.value for t in inc.scam_dna.social_engineering_tactics])

            infra = list(shared_phones) + list(shared_upis) + list(shared_urls)

            # Aggregate confidence
            cluster_rels = [
                r for r in valid_rels
                if r.source_incident_id in cluster_ids and r.target_incident_id in cluster_ids
            ]

            avg_conf = (
                sum(r.relationship_confidence for r in cluster_rels) / len(cluster_rels)
                if cluster_rels else 0.70
            )

            # Sort incidents chronologically for timeline construction
            sorted_incidents = sorted(cluster_incidents, key=lambda inc: getattr(inc, "created_at", None) or getattr(inc, "timestamp", None) or datetime.now(timezone.utc))
            
            timeline_items = []
            for inc in sorted_incidents:
                inc_infra = []
                if inc.scam_dna:
                    inc_infra = list(set(inc.scam_dna.phone_numbers + inc.scam_dna.upi_ids + inc.scam_dna.urls))
                
                channel_val = inc.channel.value if hasattr(inc.channel, "value") else str(inc.channel)
                inc_time = getattr(inc, "created_at", None) or getattr(inc, "timestamp", None) or datetime.now(timezone.utc)
                timeline_items.append(
                    TimelineItem(
                        timestamp=inc_time,
                        event_type="INCIDENT_OBSERVED",
                        channel=channel_val,
                        description=f"Incident {inc.id[:8]} observed via {channel_val.upper()} ({inc.scam_dna.impersonation_target.value if inc.scam_dna else 'unclassified'})",
                        incident_id=inc.id,
                        indicators=inc_infra,
                    )
                )

            first_seen = getattr(sorted_incidents[0], "created_at", None) or getattr(sorted_incidents[0], "timestamp", None) or datetime.now(timezone.utc)
            last_seen = getattr(sorted_incidents[-1], "created_at", None) or getattr(sorted_incidents[-1], "timestamp", None) or datetime.now(timezone.utc)

            # Risk level heuristic
            risk = RiskLevel.HIGH if len(cluster_incidents) >= 5 or len(infra) >= 3 else RiskLevel.MEDIUM

            campaign = Campaign(
                name=f"Emerging Scam Campaign ({list(shared_upis)[0] if shared_upis else 'Cluster'})",
                status=CampaignStatus.EMERGING,
                incident_ids=list(cluster_ids),
                entity_ids=[],
                relationship_ids=[r.id for r in cluster_rels],
                campaign_confidence=round(avg_conf, 4),
                risk_level=risk,
                shared_infrastructure=infra,
                shared_tactics=list(shared_tactics),
                timeline=timeline_items,
                first_seen=first_seen,
                last_seen=last_seen,
            )

            alert = CampaignAlert(
                campaign_id=campaign.id,
                alert_type="EMERGING_CAMPAIGN_DETECTED",
                incident_count=len(cluster_incidents),
                entity_count=len(infra),
                campaign_confidence=campaign.campaign_confidence,
                risk_level=risk,
                shared_infrastructure=infra,
                shared_tactics=list(shared_tactics),
                supporting_evidence=[],
            )

            results.append((campaign, alert))

        return results
