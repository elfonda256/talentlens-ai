import json

import httpx

from app.services.hr_summary import build_facts, generate_hr_summary
from tests.conftest import make_settings


def top_result(screened):
    service, job_id = screened
    results, _ = service.get_ranking(job_id)
    return (
        service.get_job(job_id),
        results[0],
        service.get_candidate(job_id, results[0].candidate_id),
    )


def gemini_client(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_without_api_key_the_deterministic_narrative_is_returned(screened, tmp_path):
    job, result, _ = top_result(screened)

    summary = generate_hr_summary(job, result, make_settings(tmp_path))

    assert summary.source == "template"
    assert summary.text == result.narrative
    assert "GEMINI_API_KEY" in summary.note


def test_gemini_receives_facts_only_and_its_text_is_returned(screened, tmp_path):
    job, result, profile = top_result(screened)
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["key"] = request.headers["x-goog-api-key"]
        seen["body"] = json.loads(request.content)
        parts = [{"text": "internal reasoning", "thought": True}, {"text": " Kandidat kuat. "}]
        return httpx.Response(200, json={"candidates": [{"content": {"parts": parts}}]})

    settings = make_settings(tmp_path, gemini_api_key="test-key", gemini_model="gemini-test")
    summary = generate_hr_summary(job, result, settings, client=gemini_client(handler))

    assert (summary.source, summary.model, summary.text) == (
        "gemini",
        "gemini-test",
        "Kandidat kuat.",
    )
    assert seen["url"].endswith("/v1beta/models/gemini-test:generateContent")
    assert seen["key"] == "test-key"
    prompt = seen["body"]["contents"][0]["parts"][0]["text"]
    assert str(result.score) in prompt and "Jangan menghitung" in prompt
    for personal_value in profile.pii.values():
        assert personal_value not in prompt


def test_facts_do_not_contain_identity_or_raw_cv(screened):
    job, result, profile = top_result(screened)

    facts = json.dumps(build_facts(job, result), ensure_ascii=False)

    assert profile.candidate_id not in facts
    assert profile.pii["name"] not in facts and profile.pii["email"] not in facts


def test_gemini_failure_falls_back_to_template(screened, tmp_path):
    job, result, _ = top_result(screened)
    settings = make_settings(tmp_path, gemini_api_key="test-key")

    failed = generate_hr_summary(
        job, result, settings, client=gemini_client(lambda request: httpx.Response(429))
    )
    empty = generate_hr_summary(
        job,
        result,
        settings,
        client=gemini_client(lambda request: httpx.Response(200, json={"candidates": []})),
    )

    assert failed.source == "template" and "HTTPStatusError" in failed.note
    assert empty.source == "template" and empty.text == result.narrative
