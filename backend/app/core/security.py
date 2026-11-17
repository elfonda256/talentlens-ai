"""Shared-key protection for the API and a server-error response that reveals nothing internal."""

import logging
import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.config import Settings, get_settings

API_KEY_HEADER = "X-API-Key"
INTERNAL_ERROR_DETAIL = "Terjadi kesalahan pada server. Coba lagi beberapa saat."

logger = logging.getLogger("talentlens.security")


def require_api_key(
    settings: Annotated[Settings, Depends(get_settings)],
    api_key: Annotated[str | None, Header(alias=API_KEY_HEADER)] = None,
) -> None:
    """Rejects a request that does not carry the shared key.

    Without a configured key (local development) every request passes; production refuses
    to start without one (see `Settings`).
    """
    if settings.api_key is None:
        return
    expected = settings.api_key.get_secret_value().encode()
    if api_key is None or not secrets.compare_digest(api_key.encode(), expected):
        raise HTTPException(401, "Kunci API tidak dikirim atau tidak valid")


async def internal_error(request: Request, error: Exception) -> JSONResponse:
    """Any unhandled error: the details stay in the server log, the client gets a plain message."""
    logger.error("Unhandled %s on %s %s", type(error).__name__, request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": INTERNAL_ERROR_DETAIL})
