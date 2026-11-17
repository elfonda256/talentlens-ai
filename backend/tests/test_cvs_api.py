import json

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app
from tests.conftest import FIXTURES, REFERENCE_DATE, SAMPLE_CVS

PARSE_URL = "/api/v1/cvs/parse"
GOLDEN = json.loads((FIXTURES / "golden_profiles.json").read_text(encoding="utf-8"))


@pytest.fixture
def client():
    app.dependency_overrides[get_settings] = lambda: Settings(reference_date=REFERENCE_DATE)
    yield TestClient(app)
    app.dependency_overrides.clear()


def upload(client, file_name, content=None):
    content = content if content is not None else (SAMPLE_CVS / file_name).read_bytes()
    return client.post(PARSE_URL, files={"file": (file_name, content)})


@pytest.mark.parametrize("file_name", ["cv_raka.pdf", "cv_nadia.docx", "cv_fajar.txt"])
def test_upload_returns_the_same_profile_as_the_service(client, file_name):
    response = upload(client, file_name)

    assert response.status_code == 200
    body = response.json()
    assert body.pop("section_confidence")["experience"] == 1.0  # added in QA Phase 2
    assert body.pop("education_in_progress") == []
    assert body == GOLDEN[file_name]


def test_unsupported_format_returns_415(client):
    response = upload(client, "cv.xlsx", b"spreadsheet")

    assert response.status_code == 415
    assert "tidak didukung" in response.json()["detail"]


def test_corrupt_document_returns_422(client):
    response = upload(client, "cv.pdf", b"%PDF-1.4 broken")

    assert response.status_code == 422
    assert response.json()["detail"] == "Dokumen rusak atau tidak dapat dibaca"


def test_oversized_file_returns_413():
    app.dependency_overrides[get_settings] = lambda: Settings(max_upload_mb=0)
    try:
        response = upload(TestClient(app), "cv_fajar.txt")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 413


def test_endpoint_is_documented_in_openapi(client):
    operation = client.get("/openapi.json").json()["paths"][PARSE_URL]["post"]

    assert operation["tags"] == ["CV"]
    assert {"200", "413", "415", "422"} <= set(operation["responses"])
