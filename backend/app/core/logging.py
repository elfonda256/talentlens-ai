"""Logging setup and the HTTP access-log middleware."""

import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
REQUEST_ID_HEADER = "X-Request-ID"

logger = logging.getLogger("talentlens.http")


def configure_logging(level: str) -> None:
    """Send all application logs to stdout in one consistent format."""
    logging.basicConfig(level=level, format=LOG_FORMAT, force=True)
    # Uvicorn's own access log would duplicate the line written by the middleware below.
    logging.getLogger("uvicorn.access").disabled = True


async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Log one line per request and return a request ID the client can quote in bug reports."""
    request_id = request.headers.get(REQUEST_ID_HEADER) or uuid.uuid4().hex[:12]
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started) * 1000
    response.headers[REQUEST_ID_HEADER] = request_id
    logger.info(
        "%s %s -> %s in %.1f ms [request_id=%s]",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_id,
    )
    return response
