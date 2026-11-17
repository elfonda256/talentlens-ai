"""Text embeddings behind one interface, with two interchangeable backends.

- e5    : intfloat/multilingual-e5-small, a small multilingual model that runs locally.
          Lets an Indonesian CV match an English job description.
- tfidf : word + character n-gram TF-IDF. No model download, works offline; the final fallback.
"""

from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Literal

import numpy as np

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

TextKind = Literal["query", "passage"]


class Embedder(ABC):
    name: str

    def fit(self, corpus: list[str]) -> None:  # noqa: B027 - only statistical backends need it
        """Learn corpus statistics. Pre-trained models ignore this."""

    @abstractmethod
    def encode(self, texts: list[str], kind: TextKind = "passage") -> np.ndarray:
        """Return one L2-normalised float32 vector per text."""

    @abstractmethod
    def calibrate(self, similarity: float) -> float:
        """Map a raw cosine similarity to 0..1 so scores are comparable across backends."""


class E5Embedder(Embedder):
    name = "multilingual-e5-small"
    # E5 cosine similarities sit in a narrow, high band. These bounds are starting values:
    # run scripts/check_ai_backends.py on real CVs and adjust if the spread looks wrong.
    SIMILARITY_FLOOR = 0.75
    SIMILARITY_CEILING = 0.88

    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str], kind: TextKind = "passage") -> np.ndarray:
        # E5 models are trained with these prefixes and lose accuracy without them.
        prefixed = [f"{kind}: {text}" for text in texts]
        vectors = self._model.encode(prefixed, normalize_embeddings=True, batch_size=32)
        return np.asarray(vectors, dtype=np.float32)

    def calibrate(self, similarity: float) -> float:
        span = self.SIMILARITY_CEILING - self.SIMILARITY_FLOOR
        return float(np.clip((similarity - self.SIMILARITY_FLOOR) / span, 0.0, 1.0))


class TfidfEmbedder(Embedder):
    name = "tfidf"

    def __init__(self, lsa_min_docs: int = 300, dims: int = 256):
        self.lsa_min_docs, self.dims = lsa_min_docs, dims
        self._pipeline = None

    def fit(self, corpus: list[str]) -> None:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.pipeline import FeatureUnion, make_pipeline
        from sklearn.preprocessing import Normalizer

        union = FeatureUnion(
            [
                ("word", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1)),
                (
                    "char",
                    TfidfVectorizer(
                        analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=1
                    ),
                ),
            ]
        )
        steps = [union]
        if len(corpus) >= self.lsa_min_docs:  # LSA is only stable on a large enough corpus
            steps.append(TruncatedSVD(n_components=self.dims, random_state=42))
        steps.append(Normalizer())
        self._pipeline = make_pipeline(*steps)
        self._pipeline.fit([bilingual(t) for t in corpus])

    def encode(self, texts: list[str], kind: TextKind = "passage") -> np.ndarray:
        if self._pipeline is None:
            raise RuntimeError("TfidfEmbedder.fit() must be called before encode()")
        matrix = self._pipeline.transform([bilingual(t) for t in texts])
        dense = matrix.todense() if hasattr(matrix, "todense") else matrix
        return np.asarray(dense, dtype=np.float32)

    def calibrate(self, similarity: float) -> float:
        return float(np.clip(similarity / 0.25, 0.0, 1.0))


@lru_cache
def _glossary() -> dict[str, str]:
    return json.loads(get_settings().glossary_path.read_text(encoding="utf-8"))


def bilingual(text: str) -> str:
    """Append English equivalents of common Indonesian words.

    Only the TF-IDF backend needs this, so an Indonesian CV can still overlap with an
    English job description. A multilingual model does not need it.
    """
    glossary = _glossary()
    tokens = re.findall(r"[a-zA-Z0-9&+#/.-]+", text.lower())
    extra = [glossary[t] for t in tokens if t in glossary]
    return " ".join(tokens + extra)


def create_embedder(settings: Settings) -> Embedder:
    """Build the configured backend. In "auto" mode, fall back to TF-IDF when E5 cannot load."""
    if settings.embedding_backend == "tfidf":
        return TfidfEmbedder()
    try:
        embedder = E5Embedder(settings.e5_model_name)
    except Exception as error:  # missing package, no network for the first download, etc.
        if settings.embedding_backend == "e5":
            raise
        logger.warning(
            "E5 embedding model unavailable (%s: %s); falling back to TF-IDF",
            type(error).__name__,
            error,
        )
        return TfidfEmbedder()
    logger.info("Loaded embedding model %s", settings.e5_model_name)
    return embedder
