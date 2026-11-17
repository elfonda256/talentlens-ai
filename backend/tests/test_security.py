"""Production hardening: shared API key, hidden docs, and no internal details in errors."""

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import create_app

KEY = "test-shared-key"


@pytest.fixture
def secured(settings, monkeypatch):
    """The app as it runs in production: a key is configured and docs are off."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("API_KEY", KEY)
    get_settings.cache_clear()
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings.model_copy(
        update={"app_env": "production", "api_key": get_settings().api_key}
    )
    yield app
    get_settings.cache_clear()


def test_health_stays_open_for_the_platform_probe(secured):
    response = TestClient(secured).get("/api/v1/health")

    assert response.status_code == 200
    assert KEY not in response.text


@pytest.mark.parametrize("headers", [{}, {"X-API-Key": "wrong"}, {"X-API-Key": ""}])
def test_requests_without_the_right_key_are_refused(secured, headers):
    client = TestClient(secured)

    for path in ("/api/v1/jobs", "/api/v1/jobs/any-job/ranking"):
        response = client.get(path, headers=headers)
        assert response.status_code == 401
        assert KEY not in response.text


def test_requests_with_the_key_are_served(secured):
    response = TestClient(secured).get("/api/v1/jobs", headers={"X-API-Key": KEY})

    assert response.status_code == 200


def test_uploads_need_the_key_too(secured):
    response = TestClient(secured).post(
        "/api/v1/jobs", files={"file": ("vacancy.txt", b"Requirements\n- AutoCAD")}
    )

    assert response.status_code == 401


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_api_docs_are_not_published_in_production(secured, path):
    assert TestClient(secured).get(path).status_code == 404


def test_api_docs_stay_available_in_development():
    client = TestClient(create_app())

    assert client.get("/openapi.json").status_code == 200


def test_production_refuses_to_start_without_a_key():
    with pytest.raises(ValueError, match="API_KEY"):
        Settings(app_env="production", api_key=None)


def test_the_key_is_never_printed_with_the_settings():
    settings = Settings(api_key=KEY)

    assert KEY not in repr(settings) and KEY not in str(settings.model_dump())


def test_an_unexpected_error_reveals_nothing_internal(secured):
    boom = APIRouter()

    @boom.get("/api/v1/boom")
    def explode():
        raise RuntimeError("database password is hunter2 at /srv/app/secret.py line 3")

    secured.include_router(boom)
    response = TestClient(secured, raise_server_exceptions=False).get("/api/v1/boom")

    assert response.status_code == 500
    assert response.json() == {"detail": "Terjadi kesalahan pada server. Coba lagi beberapa saat."}
    assert "hunter2" not in response.text and "Traceback" not in response.text


def test_cors_only_allows_the_configured_frontend(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://frontend.example.app")
    get_settings.cache_clear()
    client = TestClient(create_app())
    get_settings.cache_clear()
    preflight = {"Access-Control-Request-Method": "GET"}

    allowed = client.options(
        "/api/v1/health", headers={"Origin": "https://frontend.example.app", **preflight}
    )
    refused = client.options(
        "/api/v1/health", headers={"Origin": "https://evil.example.com", **preflight}
    )

    assert allowed.headers.get("access-control-allow-origin") == "https://frontend.example.app"
    assert "access-control-allow-origin" not in refused.headers
