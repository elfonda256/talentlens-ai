"""End-to-end API flow: job description -> CVs -> screening -> ranking -> detail -> summary."""

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.services.screening import get_screening_service
from tests.conftest import SAMPLE_CVS, SAMPLE_JOB

API = "/api/v1/jobs"


@pytest.fixture
def client(service, settings):
    app.dependency_overrides[get_screening_service] = lambda: service
    app.dependency_overrides[get_settings] = lambda: settings
    yield TestClient(app)
    app.dependency_overrides.clear()


def create_job(client) -> str:
    response = client.post(API, files={"file": ("vacancy.txt", SAMPLE_JOB.read_bytes())})
    assert response.status_code == 201
    return response.json()["job_id"]


def upload(client, job_id, *names, extra=()):
    files = [("files", (name, (SAMPLE_CVS / name).read_bytes())) for name in names]
    files += [("files", item) for item in extra]
    return client.post(f"{API}/{job_id}/candidates", files=files)


def test_job_description_is_parsed_and_listed(client):
    job_id = create_job(client)

    job = client.get(f"{API}/{job_id}").json()
    listed = client.get(API).json()

    assert job["title"] == "Junior Architect" and job["min_years_experience"] == 2
    assert listed == [
        {"job_id": job_id, "title": "Junior Architect", "candidate_count": 0, "screened": False}
    ]


def test_batch_upload_reports_each_file_separately(client):
    job_id = create_job(client)

    outcomes = upload(
        client,
        job_id,
        "cv_raka.pdf",
        "cv_nadia.docx",
        "cv_raka_reapply.txt",
        extra=[("broken.pdf", b"%PDF-1.4 broken"), ("sheet.xlsx", b"x")],
    ).json()

    assert [o["status"] for o in outcomes] == ["parsed", "parsed", "duplicate", "failed", "failed"]
    assert outcomes[2]["candidate_id"] == outcomes[0]["candidate_id"]
    assert "tidak didukung" in outcomes[4]["detail"]
    assert len(client.get(f"{API}/{job_id}/candidates").json()) == 2


def test_full_screening_flow(client):
    job_id = create_job(client)
    upload(client, job_id, "cv_raka.pdf", "cv_dimas.pdf", "cv_sinta.pdf", "cv_citra.txt")

    run = client.post(f"{API}/{job_id}/screen").json()
    ranking = client.get(f"{API}/{job_id}/ranking").json()

    assert run["screened"] == 4 and run["embedding_backend"] == "tfidf"
    assert run["shortlist"] + run["review"] + run["reject"] == 4
    scores = [row["score"] for row in ranking["results"]]
    assert scores == sorted(scores, reverse=True)
    assert [row["rank"] for row in ranking["results"]] == [1, 2, 3, 4]
    assert ranking["results"][-1]["recommendation"] == "REJECT"  # the accounting CV

    top = ranking["results"][0]
    detail = client.get(f"{API}/{job_id}/candidates/{top['candidate_id']}").json()
    assert detail["result"]["score"] == top["score"]
    assert sum(detail["result"]["contributions"].values()) == pytest.approx(top["score"], abs=0.11)
    assert detail["result"]["reasons"] and detail["result"]["evidence"]
    assert detail["experiences"] and detail["skills"]

    summary = client.post(f"{API}/{job_id}/candidates/{top['candidate_id']}/summary").json()
    assert summary["source"] == "template" and summary["text"] == detail["result"]["narrative"]


def test_identities_are_hidden_unless_revealed(client):
    job_id = create_job(client)
    upload(client, job_id, "cv_raka.pdf")
    client.post(f"{API}/{job_id}/screen")
    candidate_id = client.get(f"{API}/{job_id}/ranking").json()["results"][0]["candidate_id"]

    blind = client.get(f"{API}/{job_id}/ranking").json()["results"][0]
    revealed = client.get(f"{API}/{job_id}/ranking?reveal=true").json()["results"][0]
    blind_detail = client.get(f"{API}/{job_id}/candidates/{candidate_id}").json()
    revealed_detail = client.get(f"{API}/{job_id}/candidates/{candidate_id}?reveal=true").json()

    assert (blind["name"], blind["file_name"]) == ("", "")
    assert (revealed["name"], revealed["file_name"]) == ("Raka Pratama", "cv_raka.pdf")
    assert blind_detail["identity"] == {}
    assert revealed_detail["identity"]["email"] == "raka.pratama@example.com"


def test_new_upload_invalidates_the_previous_ranking(client):
    job_id = create_job(client)
    upload(client, job_id, "cv_raka.pdf")
    client.post(f"{API}/{job_id}/screen")

    upload(client, job_id, "cv_nadia.docx")

    assert client.get(f"{API}/{job_id}/ranking").status_code == 409
    assert client.get(API).json()[0]["screened"] is False


def test_error_responses(client):
    job_id = create_job(client)

    assert client.get(f"{API}/unknown").status_code == 404
    assert client.post(f"{API}/unknown/screen").status_code == 404
    assert client.post(f"{API}/{job_id}/screen").status_code == 409  # no candidates yet
    assert client.get(f"{API}/{job_id}/ranking").status_code == 409  # not screened yet
    assert client.post(API, files={"file": ("jd.xlsx", b"x")}).status_code == 415
    assert client.post(API, files={"file": ("jd.txt", b"short")}).status_code == 422

    upload(client, job_id, "cv_raka.pdf")
    client.post(f"{API}/{job_id}/screen")
    assert client.get(f"{API}/{job_id}/candidates/C-NOPE").status_code == 404
    assert client.post(f"{API}/{job_id}/candidates/C-NOPE/summary").status_code == 404


def test_results_survive_a_restart(service, settings):
    from app.services.screening import ScreeningService
    from app.services.store import JsonStore

    job = service.create_job(SAMPLE_JOB)
    service.add_candidate(job.job_id, SAMPLE_CVS / "cv_raka.pdf", "cv_raka.pdf")
    before, _ = service.screen(job.job_id)

    reopened = ScreeningService(JsonStore(settings.storage_dir / "state.json"), settings)
    after, backend = reopened.get_ranking(job.job_id)

    assert after == before and backend == "tfidf"
