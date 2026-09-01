"""
ScamTrap AI — Health Endpoint Tests

Gate check: health endpoint returns 200 OK with expected fields.
"""


def test_health_returns_200(client):
    """Health endpoint should return 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_fields(client):
    """Health response must contain all required fields."""
    response = client.get("/health")
    data = response.json()

    required_fields = [
        "status",
        "app_name",
        "version",
        "uptime_seconds",
        "started_at",
        "timestamp",
        "llm_provider",
        "embedding_provider",
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"


def test_health_status_ok(client):
    """Health status should be 'ok'."""
    response = client.get("/health")
    assert response.json()["status"] == "ok"


def test_health_app_name(client):
    """Health should report the correct app name."""
    response = client.get("/health")
    assert response.json()["app_name"] == "ScamTrap AI"


def test_health_api_v1_path(client):
    """Health should also be available at /api/v1/health."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_request_id_header(client):
    """Response should include X-Request-ID header."""
    response = client.get("/health")
    assert "X-Request-ID" in response.headers


def test_health_custom_request_id(client):
    """Custom X-Request-ID should be echoed back."""
    custom_id = "test-request-12345"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.headers["X-Request-ID"] == custom_id
