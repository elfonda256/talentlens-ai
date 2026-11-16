"""Application entry point.  Run with: uvicorn app.main:app --reload"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import REQUEST_ID_HEADER, configure_logging, log_requests

DESCRIPTION = (
    "AI recruitment copilot: parses CVs and job descriptions, matches them semantically, "
    "ranks candidates and explains every score."
)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name, version=settings.app_version, description=DESCRIPTION)
    app.middleware("http")(log_requests)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[REQUEST_ID_HEADER],
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
