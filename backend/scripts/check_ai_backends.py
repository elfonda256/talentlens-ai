"""Checks the two AI components that need the internet: the E5 model and the Gemini API.

Run from the backend folder:  python scripts/check_ai_backends.py

It prints what works on THIS machine with the current environment, so a problem is found
before a demo rather than during it. Nothing is stored.
"""

from __future__ import annotations

import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import get_settings  # noqa: E402
from app.services.embedding import E5Embedder  # noqa: E402

REQUIREMENT = "Architect with minimum 2 years experience in design and build"
RELATED = "Arsitek junior dengan pengalaman 3 tahun pada proyek desain dan bangun"
UNRELATED = "Staf akuntansi yang menyusun laporan pajak bulanan"


def check_e5(model_name: str) -> bool:
    print(f"[E5] Loading {model_name} (the first run downloads about 470 MB)...")
    try:
        embedder = E5Embedder(model_name)
    except Exception as error:
        print(f"[E5] FAILED: {type(error).__name__}: {error}")
        print("[E5] Install it with: pip install -r requirements-e5.txt")
        return False
    query = embedder.encode([REQUIREMENT], kind="query")[0]
    related, unrelated = embedder.encode([RELATED, UNRELATED], kind="passage") @ query
    print(f"[E5] OK. English requirement vs Indonesian CV line: {related:.3f}")
    print(f"[E5]     English requirement vs unrelated line:     {unrelated:.3f}")
    low, high = embedder.SIMILARITY_FLOOR, embedder.SIMILARITY_CEILING
    scores = f"{embedder.calibrate(related):.2f} and {embedder.calibrate(unrelated):.2f}"
    print(f"[E5] Calibrated: {scores}. The related line should be clearly higher.")
    print(f"[E5] If both are near 0 or 1, adjust the band ({low}-{high}) in embedding.py.")
    return related > unrelated


def check_gemini(api_key: str, model: str, timeout: float) -> bool:
    if not api_key:
        print("[Gemini] SKIPPED: GEMINI_API_KEY is not set (summaries will use the template).")
        return False
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"contents": [{"parts": [{"text": "Balas dengan satu kata: siap"}]}]}
    try:
        response = httpx.post(url, headers={"x-goog-api-key": api_key}, json=body, timeout=timeout)
        response.raise_for_status()
        parts = response.json()["candidates"][0]["content"]["parts"]
    except httpx.HTTPStatusError as error:
        print(f"[Gemini] FAILED: HTTP {error.response.status_code}: {error.response.text[:300]}")
        print("[Gemini] A 404 usually means the model name is wrong: set GEMINI_MODEL.")
        return False
    except (httpx.HTTPError, KeyError, IndexError) as error:
        print(f"[Gemini] FAILED: {type(error).__name__}: {error}")
        return False
    answer = "".join(part.get("text", "") for part in parts).strip()
    print(f"[Gemini] OK. {model} answered: {answer!r}")
    return True


def main() -> int:
    settings = get_settings()
    e5_ok = check_e5(settings.e5_model_name)
    gemini_ok = check_gemini(
        settings.gemini_api_key, settings.gemini_model, settings.gemini_timeout_seconds
    )
    status = {True: "OK", False: "NOT AVAILABLE"}
    print(f"\nSummary: E5 {status[e5_ok]}, Gemini {status[gemini_ok]}")
    return 0 if e5_ok and gemini_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
