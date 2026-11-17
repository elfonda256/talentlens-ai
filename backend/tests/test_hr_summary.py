import json

import httpx

from app.services.hr_summary import build_facts, generate_hr_summary, template_note
from app.services.match_breakdown import build_breakdown
from tests.conftest import make_settings

GEMINI_NOTE = {
    "headline": "Kandidat ini layak diwawancarai.",
    "fit": "Pengalamannya sejalan dengan kebutuhan posisi.",
    "strengths": ["Terbiasa dengan AutoCAD.", "  ", "Berpengalaman di proyek desain dan bangun."],
    "concerns": [],
    "risks": ["Belum ada bukti pengalaman memimpin."],
    "interview_focus": ["Gali perannya di proyek terakhir."],
    "recommendation_reason": "Syarat utama terpenuhi.",
}


def case(screened, file_name=None, position=0):
    """(job, profile, result, breakdown) for one candidate of the screened sample job."""
    service, job_id = screened
    results, _ = service.get_ranking(job_id)
    job = service.get_job(job_id)
    if file_name:
        profile = next(c for c in service.list_candidates(job_id) if c.file_name == file_name)
        result = service.get_result(job_id, profile.candidate_id)
    else:
        result = results[position]
        profile = service.get_candidate(job_id, result.candidate_id)
    return job, profile, result, build_breakdown(job, profile, result)


def answer(text: str):
    """A stand-in Gemini that always replies with the given text."""
    payload = {"candidates": [{"content": {"parts": [{"text": text}]}}]}
    return httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, json=payload)))


def test_without_api_key_the_template_fills_every_section(screened, tmp_path):
    job, profile, result, breakdown = case(screened, "cv_raka.pdf")

    summary = generate_hr_summary(job, profile, result, breakdown, make_settings(tmp_path))

    assert summary.source == "template" and "GEMINI_API_KEY" in summary.note
    assert summary.headline == (
        "Kandidat kuat untuk Junior Architect: 3,2 tahun pengalaman relevan "
        "dan 9 dari 9 keterampilan wajib terpenuhi."
    )
    assert "9 dari 9 keterampilan wajib" in summary.fit and "3,2 tahun" in summary.fit
    assert any("AutoCAD" in item for item in summary.strengths)
    assert any("Junior Architect" in item for item in summary.strengths)  # the relevant role
    assert summary.interview_focus and summary.recommendation_reason
    assert "poin" not in json.dumps(summary.model_dump(), ensure_ascii=False)  # no scoring jargon


def test_template_follows_the_recommendation_and_names_the_gaps(screened):
    job, profile, result, breakdown = case(screened, "cv_citra.txt")  # an accountant, rejected
    rejected = template_note(job, profile, result, breakdown)
    job, profile, result, breakdown = case(screened, "cv_sinta.pdf")  # a graduate, under review
    review = template_note(job, profile, result, breakdown)

    assert rejected.headline.startswith("Belum sesuai untuk Junior Architect: ")
    assert any("berbeda dari yang diminta (akuntansi)" in item for item in rejected.concerns)
    assert rejected.interview_focus == []  # nothing to prepare for a rejected candidate
    assert review.headline.startswith("Kandidat potensial untuk Junior Architect, dengan catatan:")
    assert any("di bawah syarat 2 tahun" in item for item in review.concerns)
    assert any("berapa lama" in item for item in review.interview_focus)
    assert all(item.endswith("?") for item in review.interview_focus)  # questions, ready to ask


def test_scanned_cv_is_reported_as_a_risk(service):
    from tests.conftest import SAMPLE_CVS, SAMPLE_JOB

    job = service.create_job(SAMPLE_JOB)
    profile, _ = service.add_candidate(job.job_id, SAMPLE_CVS / "cv_raka.pdf", "cv_raka.pdf")
    service.screen(job.job_id)
    result = service.get_result(job.job_id, profile.candidate_id)
    scanned = profile.model_copy(update={"extraction_method": "ocr"})

    note = template_note(job, scanned, result, build_breakdown(job, scanned, result))

    assert any("hasil scan" in item for item in note.risks)


def test_gemini_note_is_used_and_cleaned(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    settings = make_settings(tmp_path, gemini_api_key="test-key", gemini_model="gemini-test")
    fenced = "```json\n" + json.dumps(GEMINI_NOTE, ensure_ascii=False) + "\n```"

    summary = generate_hr_summary(job, profile, result, breakdown, settings, client=answer(fenced))

    assert (summary.source, summary.model) == ("gemini", "gemini-test")
    assert summary.headline == GEMINI_NOTE["headline"]
    assert summary.strengths == [
        "Terbiasa dengan AutoCAD.",
        "Berpengalaman di proyek desain dan bangun.",
    ]
    assert summary.concerns == []


def test_gemini_receives_facts_only(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["key"] = request.headers["x-goog-api-key"]
        seen["prompt"] = json.loads(request.content)["contents"][0]["parts"][0]["text"]
        parts = [{"text": "thinking", "thought": True}, {"text": json.dumps(GEMINI_NOTE)}]
        return httpx.Response(200, json={"candidates": [{"content": {"parts": parts}}]})

    settings = make_settings(tmp_path, gemini_api_key="test-key", gemini_model="gemini-test")
    client = httpx.Client(transport=httpx.MockTransport(handler))
    summary = generate_hr_summary(job, profile, result, breakdown, settings, client=client)

    assert summary.source == "gemini"
    assert seen["url"].endswith("/v1beta/models/gemini-test:generateContent")
    assert seen["key"] == "test-key"
    assert str(result.score) in seen["prompt"]
    assert "Jangan menghitung, mengubah, atau menilai ulang skor" in seen["prompt"]
    for personal_value in profile.pii.values():
        assert personal_value not in seen["prompt"]


def test_facts_do_not_contain_identity(screened):
    job, profile, result, breakdown = case(screened, "cv_raka.pdf")

    facts = json.dumps(build_facts(job, result, breakdown), ensure_ascii=False)

    assert profile.candidate_id not in facts
    assert profile.pii["name"] not in facts and profile.pii["email"] not in facts
    assert '"pengalaman_relevan_tahun": 3.2' in facts


def test_unusable_gemini_answers_fall_back_to_the_same_shape(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    settings = make_settings(tmp_path, gemini_api_key="test-key")
    expected = template_note(job, profile, result, breakdown)
    failing = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(429)))
    incomplete = json.dumps({"headline": "Hanya judul"})

    for client in (failing, answer("Maaf, saya tidak bisa."), answer(incomplete), answer("")):
        summary = generate_hr_summary(job, profile, result, breakdown, settings, client=client)

        assert summary.source == "template" and "Gemini tidak dapat dipakai" in summary.note
        assert summary.headline == expected.headline
        assert summary.strengths == expected.strengths


def scripted(*replies):
    """A stand-in Gemini that answers each request with the next reply and records the URLs.
    A reply is a status code, an exception to raise, or a note dict returned with 200."""
    calls: list[str] = []
    queue = list(replies)

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path.rsplit("/", 1)[-1].split(":")[0])
        reply = queue.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if isinstance(reply, int):
            return httpx.Response(reply, json={"error": {"code": reply}})
        parts = [{"text": json.dumps(reply)}]
        return httpx.Response(200, json={"candidates": [{"content": {"parts": parts}}]})

    return httpx.Client(transport=httpx.MockTransport(handler)), calls


def gemini_settings(tmp_path):
    return make_settings(
        tmp_path, gemini_api_key="test-key", gemini_model="main", gemini_fallback_model="lite"
    )


def test_request_asks_for_json_with_low_thinking(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen.update(json.loads(request.content)["generationConfig"])
        parts = [{"text": json.dumps(GEMINI_NOTE)}]
        return httpx.Response(200, json={"candidates": [{"content": {"parts": parts}}]})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    generate_hr_summary(job, profile, result, breakdown, gemini_settings(tmp_path), client=client)

    assert seen == {
        "responseMimeType": "application/json",
        "thinkingConfig": {"thinkingLevel": "low"},
    }


def test_overloaded_model_is_retried(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    client, calls = scripted(503, GEMINI_NOTE)

    summary = generate_hr_summary(
        job, profile, result, breakdown, gemini_settings(tmp_path), client=client
    )

    assert (summary.source, summary.model) == ("gemini", "main")
    assert calls == ["main", "main"]


def test_timeouts_fall_back_to_the_lighter_model(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    timeout = httpx.ReadTimeout("slow")
    client, calls = scripted(timeout, timeout, GEMINI_NOTE)

    summary = generate_hr_summary(
        job, profile, result, breakdown, gemini_settings(tmp_path), client=client
    )

    assert (summary.source, summary.model) == ("gemini", "lite")
    assert calls == ["main", "main", "lite"]


def test_retired_model_goes_straight_to_the_fallback(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    client, calls = scripted(404, GEMINI_NOTE)

    summary = generate_hr_summary(
        job, profile, result, breakdown, gemini_settings(tmp_path), client=client
    )

    assert summary.model == "lite" and calls == ["main", "lite"]


def test_rejected_request_is_not_retried(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    client, calls = scripted(400)

    summary = generate_hr_summary(
        job, profile, result, breakdown, gemini_settings(tmp_path), client=client
    )

    assert summary.source == "template" and calls == ["main"]


def test_every_attempt_failing_uses_the_template(screened, tmp_path):
    job, profile, result, breakdown = case(screened)
    client, calls = scripted(503, httpx.ConnectError("down"), 503)

    summary = generate_hr_summary(
        job, profile, result, breakdown, gemini_settings(tmp_path), client=client
    )

    assert summary.source == "template" and "HTTPStatusError" in summary.note
    assert calls == ["main", "main", "lite"]
