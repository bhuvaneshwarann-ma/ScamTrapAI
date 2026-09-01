"""
ScamTrap AI — Phase 12 API Gateway Tests

Validates:
- Incident ingestion POST /api/v1/incidents
- Listing incidents GET /api/v1/incidents
- Incident detail and ScamDNA endpoints
- Auth login & logout
- Evaluation metrics endpoint
"""

import pytest


def test_auth_login(client):
    res = client.post("/auth/login", json={"email": "investigator@scamtrap.ai", "password": "password123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "investigator"


def test_create_and_get_incident(client):
    payload = {
        "raw_text": "SBI ALERT: Your account is blocked. Update PAN card at https://sbi-kyc-portal.xyz/pay or send fee to sbi.kyc@ybl.",
        "channel": "sms"
    }
    res = client.post("/api/v1/incidents", json=payload)
    assert res.status_code == 200
    inc_data = res.json()
    assert inc_data["id"] is not None
    assert inc_data["scam_dna"] is not None
    assert inc_data["scam_dna"]["impersonation_target"] == "bank"

    # List incidents
    res_list = client.get("/api/v1/incidents")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # Get single incident
    res_single = client.get(f"/api/v1/incidents/{inc_data['id']}")
    assert res_single.status_code == 200
    assert res_single.json()["id"] == inc_data["id"]

    # Get incident DNA
    res_dna = client.get(f"/api/v1/incidents/{inc_data['id']}/dna")
    assert res_dna.status_code == 200
    assert res_dna.json()["impersonation_target"] == "bank"


def test_metrics_endpoint(client):
    res = client.get("/api/v1/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "dataset_size" in data
    assert "relationship_precision" in data
    assert "relationship_f1" in data
    assert "false_similarity_rejected" in data
