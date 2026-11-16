"""Skill taxonomy: maps spelling variants found in text to canonical skill ids."""

from __future__ import annotations

import json
import re
from functools import lru_cache

from app.core.config import get_settings


@lru_cache
def load() -> dict[str, dict]:
    return json.loads(get_settings().taxonomy_path.read_text(encoding="utf-8"))


@lru_cache
def _patterns() -> list[tuple[str, re.Pattern]]:
    patterns = []
    for skill_id, meta in load().items():
        alts = sorted({a.lower() for a in meta["aliases"]}, key=len, reverse=True)
        body = "|".join(re.escape(a) for a in alts)
        patterns.append(
            (skill_id, re.compile(rf"(?<![a-z0-9])(?:{body})(?![a-z0-9])", re.IGNORECASE))
        )
    return patterns


def find_skills(text: str) -> list[str]:
    return [skill_id for skill_id, pattern in _patterns() if pattern.search(text)]
