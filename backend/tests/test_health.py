from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app

client = TestClient(app)


def test_health_reports_ok_with_app_metadata():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app_name"] == "TalentLens AI"
    assert set(body) == {
        "status",
        "app_name",
        "version",
        "environment",
        "timestamp",
        "embedding_backend",
        "llm_summary",
    }


def test_every_response_carries_a_request_id():
    response = client.get("/api/v1/health", headers={"X-Request-ID": "demo-123"})

    assert response.headers["X-Request-ID"] == "demo-123"
    assert client.get("/api/v1/health").headers["X-Request-ID"]


def test_cors_allows_the_configured_frontend_origin():
    response = client.get("/api/v1/health", headers={"Origin": "http://localhost:3000"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_swagger_and_openapi_are_served():
    assert client.get("/docs").status_code == 200
    assert "/api/v1/health" in client.get("/openapi.json").json()["paths"]


def test_settings_are_overridden_by_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("CORS_ORIGINS", "http://a.test, http://b.test")
    get_settings.cache_clear()
    try:
        settings = get_settings()
        assert isinstance(settings, Settings)
        assert settings.app_env == "test"
        assert settings.cors_origin_list == ["http://a.test", "http://b.test"]
    finally:
        get_settings.cache_clear()
