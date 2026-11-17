"""Application entry point.  Run with: uvicorn app.main:app --reload"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import REQUEST_ID_HEADER, configure_logging, log_requests
from app.core.security import API_KEY_HEADER, internal_error

DESCRIPTION = (
    "AI recruitment copilot: parses CVs and job descriptions, matches them semantically, "
    "ranks candidates and explains every score."
)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    # Interactive docs describe every endpoint; production does not publish them.
    docs = not settings.is_production
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=DESCRIPTION,
        docs_url="/docs" if docs else None,
        redoc_url="/redoc" if docs else None,
        openapi_url="/openapi.json" if docs else None,
    )
    app.add_exception_handler(Exception, internal_error)
    app.middleware("http")(log_requests)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", API_KEY_HEADER, REQUEST_ID_HEADER],
        expose_headers=[REQUEST_ID_HEADER],
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
