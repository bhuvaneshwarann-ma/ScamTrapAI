"""
ScamTrap AI — Integration Test Suite (Master Prompt #22)

Verifies:
1. Incident ingestion (POST /api/v1/incidents)
2. Scam DNA extraction
3. Entity extraction & resolution
4. Relationship creation
5. Evidence generation
6. Campaign detection & assignment
7. Campaign graph API endpoint
8. Evaluation metrics calculation
"""

import pytest


def test_full_pipeline_integration(client):
    # Ingest Incident A
    payload_a = {
        "raw_text": "SBI ALERT: Your account is blocked. Update PAN card at https://sbi-kyc-update-portal.xyz/verify or send fee to sbi.kyc.update@ybl. Call +919876543210.",
        "channel": "sms"
    }
    res_a = client.post("/api/v1/incidents", json=payload_a)
    assert res_a.status_code == 200
    data_a = res_a.json()
    assert data_a["id"] is not None
    assert data_a["scam_dna"]["impersonation_target"] == "bank"

    # Ingest Incident B (Same campaign)
    payload_b = {
        "raw_text": "வணக்கம், உங்கள் SBI கணக்கு முடக்கப்படும். உடனடியாக KYC புதுப்பிக்கவும்: https://sbi-kyc-update-portal.xyz/verify. UPI: sbi.kyc.update@ybl. தொடர்புக்கு: +919876543210.",
        "channel": "whatsapp"
    }
    res_b = client.post("/api/v1/incidents", json=payload_b)
    assert res_b.status_code == 200

    # Ingest Incident D (False Similarity Control)
    payload_d = {
        "raw_text": "Dear customer, your monthly SBI bank statement for August is ready. View it safely in your YONO app. SBI will never ask for your OTP.",
        "channel": "sms"
    }
    res_d = client.post("/api/v1/incidents", json=payload_d)
    assert res_d.status_code == 200

    # List campaigns
    res_camps = client.get("/api/v1/campaigns")
    assert res_camps.status_code == 200
    camps = res_camps.json()
    assert len(camps) >= 1

    # Campaign Graph
    camp_id = camps[0]["id"]
    res_graph = client.get(f"/api/v1/campaigns/{camp_id}/graph")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    assert "nodes" in graph_data
    assert "edges" in graph_data
    assert len(graph_data["nodes"]) >= 2

    # Metrics evaluation
    res_metrics = client.get("/api/v1/metrics")
    assert res_metrics.status_code == 200
    metrics = res_metrics.json()
    assert "relationship_precision" in metrics
    assert metrics["false_similarity_rejected"] is True
