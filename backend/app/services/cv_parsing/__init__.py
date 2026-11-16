"""Public interface of the CV parsing service."""

from app.services.cv_parsing.document_loader import SUPPORTED_SUFFIXES, UnsupportedFormatError
from app.services.cv_parsing.service import UnreadableDocumentError, parse_cv

__all__ = ["SUPPORTED_SUFFIXES", "UnreadableDocumentError", "UnsupportedFormatError", "parse_cv"]
