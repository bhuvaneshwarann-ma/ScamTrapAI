"""
ScamTrap AI — Campaign Graph Engine (Phase 8)

Builds NetworkX-based heterogeneous multi-graphs representing incident and entity relationships.
Nodes: Incident, Phone, UPI, URL, Domain, ScamDNA, Campaign.
Edges: USES_PHONE, USES_UPI, USES_URL, USES_DOMAIN, SIMILAR_TO, RELATED_TO, MEMBER_OF.

Provides:
- `GraphBuilder`: Ingests incidents & relationships into NetworkX graph.
- `GraphQueryService`: React Flow payload generation with evidence metadata on edges.
- `GraphAnalyticsService`: Connected components & community detection.
"""

from typing import Any, Dict, List, Set, Tuple
import networkx as nx

from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship


class GraphEngine:
    """NetworkX-backed heterogeneous campaign graph engine."""

    def __init__(self):
        self.graph = nx.Graph()

    def build_graph(self, incidents: List[Incident], relationships: List[Relationship]) -> nx.Graph:
        """Construct graph from incidents and verified relationships."""
        self.graph.clear()

        # Add Incident & Entity nodes
        for inc in incidents:
            self.graph.add_node(
                inc.id,
                type="incident",
                label=f"Incident {inc.id[:8]}",
                channel=inc.channel.value if hasattr(inc.channel, "value") else str(inc.channel),
                ground_truth=inc.ground_truth_campaign_id,
            )

            if inc.scam_dna:
                # Add extracted entity nodes and edges
                for phone in inc.scam_dna.phone_numbers:
                    p_id = f"phone:{phone}"
                    self.graph.add_node(p_id, type="phone", label=phone)
                    self.graph.add_edge(inc.id, p_id, relation="USES_PHONE")

                for upi in inc.scam_dna.upi_ids:
                    u_id = f"upi:{upi}"
                    self.graph.add_node(u_id, type="upi", label=upi)
                    self.graph.add_edge(inc.id, u_id, relation="USES_UPI")

                for url in inc.scam_dna.urls:
                    url_id = f"url:{url}"
                    self.graph.add_node(url_id, type="url", label=url)
                    self.graph.add_edge(inc.id, url_id, relation="USES_URL")

        # Add Relationship edges
        for rel in relationships:
            if self.graph.has_node(rel.source_incident_id) and self.graph.has_node(rel.target_incident_id):
                evidence_count = len(rel.supporting_evidence)
                self.graph.add_edge(
                    rel.source_incident_id,
                    rel.target_incident_id,
                    relation=rel.relationship_type.value if hasattr(rel.relationship_type, "value") else str(rel.relationship_type),
                    probability=rel.relationship_probability,
                    confidence=rel.relationship_confidence,
                    evidence_count=evidence_count,
                    is_verified=rel.is_verified,
                )

        return self.graph

    def get_clusters(self) -> List[Set[str]]:
        """Find connected incident components (candidate campaigns)."""
        incident_nodes = [n for n, d in self.graph.nodes(data=True) if d.get("type") == "incident"]
        subgraph = self.graph.subgraph(incident_nodes)
        components = [c for c in nx.connected_components(subgraph) if len(c) > 1]
        return components

    def to_react_flow_json(self) -> Dict[str, List[Dict[str, Any]]]:
        """Format graph for React Flow visualization UI."""
        nodes = []
        edges = []

        for node_id, data in self.graph.nodes(data=True):
            nodes.append({
                "id": node_id,
                "type": data.get("type", "default"),
                "data": {"label": data.get("label", node_id), **data},
            })

        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "id": f"e-{u}-{v}",
                "source": u,
                "target": v,
                "label": data.get("relation", "RELATED"),
                "data": data,
            })

        return {"nodes": nodes, "edges": edges}
