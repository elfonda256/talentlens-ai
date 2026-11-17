import numpy as np
import pytest

from app.services.vector_index import FaissIndex


def unit(*values: float) -> np.ndarray:
    vector = np.array(values, dtype=np.float32)
    return vector / np.linalg.norm(vector)


@pytest.fixture
def index() -> FaissIndex:
    idx = FaissIndex()
    idx.add("A", np.stack([unit(1, 0, 0), unit(0, 1, 0)]), ["a-first", "a-second"])
    idx.add("B", np.stack([unit(0, 0, 1), unit(1, 1, 0)]), ["b-first", "b-second"])
    return idx


def test_search_returns_cosine_similarity_in_descending_order(index):
    hits = index.search(unit(1, 0.2, 0), top_k=3)

    assert [h.text for h in hits] == ["a-first", "b-second", "a-second"]
    assert hits[0].score == pytest.approx(0.9806, abs=1e-3)
    assert hits[0].candidate_id == "A"


def test_best_match_is_restricted_to_one_candidate(index):
    query = unit(0, 0, 1)  # globally closest to B's first chunk

    assert index.search(query, top_k=1)[0].text == "b-first"
    assert index.best_match(query, "A").candidate_id == "A"
    assert index.best_match(query, "B").text == "b-first"


def test_unknown_candidate_and_empty_index_return_nothing(index):
    assert index.best_match(unit(1, 0, 0), "missing") is None
    assert FaissIndex().search(unit(1, 0, 0), top_k=5) == []


def test_candidate_without_chunks_is_skipped_and_duplicates_are_rejected(index):
    index.add("C", np.empty((0, 3), dtype=np.float32), [])

    assert len(index) == 4
    with pytest.raises(ValueError):
        index.add("A", np.stack([unit(1, 0, 0)]), ["again"])
