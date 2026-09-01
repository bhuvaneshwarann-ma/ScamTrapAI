"""
ScamTrap AI — CTI API & MITRE ATT&CK Test Suite

Validates:
- Unified IOC search endpoint (GET /api/v1/cti/ioc-search)
- MITRE ATT&CK heatmap matrix endpoint (GET /api/v1/cti/mitre-matrix)
- CTI threat feeds endpoint (GET /api/v1/cti/threat-feeds)
"""

import pytest


def test_ioc_search_endpoint(client):
    res = client.get("/api/v1/cti/ioc-search?query=sbi.kyc.update@ybl")
    assert res.status_code == 200
    data = res.json()
    assert "ioc_value" in data
    assert data["threat_score"] >= 70
    assert "associated_campaign_ids" in data


def test_mitre_matrix_endpoint(client):
    res = client.get("/api/v1/cti/mitre-matrix")
    assert res.status_code == 200
    data = res.json()
    assert "tactics" in data
    assert "Initial Access" in data["tactics"]
    assert data["total_techniques_detected"] >= 4


def test_threat_feeds_endpoint(client):
    res = client.get("/api/v1/cti/threat-feeds")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 2
    assert "indicator" in data[0]
