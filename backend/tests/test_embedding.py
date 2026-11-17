import sys
import types

import numpy as np
import pytest

from app.services import embedding
from app.services.embedding import E5Embedder, TfidfEmbedder, bilingual, create_embedder
from tests.conftest import make_settings


def test_tfidf_vectors_are_normalised_and_rank_related_text_higher():
    embedder = TfidfEmbedder()
    corpus = ["technical drawing in AutoCAD", "monthly tax report", "construction drawing"]
    embedder.fit(corpus)

    vectors = embedder.encode(corpus)
    query = embedder.encode(["AutoCAD drawing"], kind="query")[0]

    assert np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5)
    assert vectors.dtype == np.float32
    assert vectors[0] @ query > vectors[2] @ query > vectors[1] @ query


def test_tfidf_must_be_fitted_first():
    with pytest.raises(RuntimeError):
        TfidfEmbedder().encode(["text"])


def test_bilingual_adds_english_equivalents_for_indonesian_words():
    assert "drawing" in bilingual("Menyusun gambar kerja").split()
    assert bilingual("AutoCAD") == "autocad"


def test_calibration_is_clipped_to_unit_range():
    assert TfidfEmbedder().calibrate(0.5) == 1.0
    assert TfidfEmbedder().calibrate(0.125) == pytest.approx(0.5)
    assert TfidfEmbedder().calibrate(-0.1) == 0.0


def test_auto_mode_falls_back_to_tfidf_when_e5_cannot_load(tmp_path, monkeypatch, caplog):
    def fail(self, model_name):
        raise OSError("model files are not available")

    monkeypatch.setattr(E5Embedder, "__init__", fail)

    with caplog.at_level("WARNING", logger=embedding.__name__):
        embedder = create_embedder(make_settings(tmp_path, embedding_backend="auto"))

    assert embedder.name == "tfidf"
    assert "falling back to TF-IDF" in caplog.text


def test_explicit_e5_mode_does_not_hide_a_loading_error(tmp_path, monkeypatch):
    def fail(self, model_name):
        raise OSError("model files are not available")

    monkeypatch.setattr(E5Embedder, "__init__", fail)

    with pytest.raises(OSError):
        create_embedder(make_settings(tmp_path, embedding_backend="e5"))


def test_e5_wrapper_adds_prefixes_and_requests_normalised_vectors(monkeypatch):
    """Checks the wrapper around sentence-transformers with a stand-in model (no download)."""
    calls = {}

    class StandInModel:
        def __init__(self, name):
            calls["model"] = name

        def encode(self, texts, normalize_embeddings, batch_size):
            calls["texts"], calls["normalize"] = texts, normalize_embeddings
            return [[1.0, 0.0]] * len(texts)

    module = types.ModuleType("sentence_transformers")
    module.SentenceTransformer = StandInModel
    monkeypatch.setitem(sys.modules, "sentence_transformers", module)

    embedder = E5Embedder("intfloat/multilingual-e5-small")
    vectors = embedder.encode(["minimum 2 years experience"], kind="query")
    embedder.encode(["Arsitek junior"], kind="passage")

    assert calls["model"] == "intfloat/multilingual-e5-small"
    assert calls["texts"] == ["passage: Arsitek junior"]
    assert calls["normalize"] is True
    assert vectors.shape == (1, 2) and vectors.dtype == np.float32
    assert embedder.calibrate(0.75) == 0.0 and embedder.calibrate(0.88) == pytest.approx(1.0)
