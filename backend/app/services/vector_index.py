"""FAISS vector index over CV chunks.

Vectors are L2-normalised, so the inner product computed by IndexFlatIP is the cosine
similarity. Each candidate's chunks are added as one contiguous block, which lets a search
be restricted to a single candidate with an id range.
"""

from __future__ import annotations

from dataclasses import dataclass

import faiss
import numpy as np


@dataclass(frozen=True)
class Hit:
    candidate_id: str
    text: str
    score: float


class FaissIndex:
    def __init__(self) -> None:
        self._index: faiss.IndexFlatIP | None = None
        self._texts: list[str] = []
        self._owners: list[str] = []
        self._ranges: dict[str, tuple[int, int]] = {}

    def __len__(self) -> int:
        return len(self._texts)

    def add(self, candidate_id: str, vectors: np.ndarray, texts: list[str]) -> None:
        if candidate_id in self._ranges:
            raise ValueError(f"Candidate {candidate_id} is already indexed")
        if len(texts) == 0:
            return
        if self._index is None:
            self._index = faiss.IndexFlatIP(vectors.shape[1])
        start = len(self._texts)
        self._index.add(np.ascontiguousarray(vectors, dtype=np.float32))
        self._texts += texts
        self._owners += [candidate_id] * len(texts)
        self._ranges[candidate_id] = (start, start + len(texts))

    def search(self, vector: np.ndarray, top_k: int) -> list[Hit]:
        """Most similar chunks across all candidates."""
        return self._search(vector, top_k, None)

    def best_match(self, vector: np.ndarray, candidate_id: str) -> Hit | None:
        """The single most similar chunk belonging to one candidate."""
        id_range = self._ranges.get(candidate_id)
        if id_range is None:
            return None
        hits = self._search(vector, 1, faiss.IDSelectorRange(*id_range))
        return hits[0] if hits else None

    def _search(self, vector: np.ndarray, top_k: int, selector) -> list[Hit]:
        if self._index is None:
            return []
        query = np.ascontiguousarray(vector.reshape(1, -1), dtype=np.float32)
        params = faiss.SearchParameters(sel=selector) if selector is not None else None
        scores, ids = self._index.search(query, min(top_k, len(self._texts)), params=params)
        return [
            Hit(self._owners[i], self._texts[i], float(score))
            for score, i in zip(scores[0], ids[0], strict=True)
            if i != -1
        ]
