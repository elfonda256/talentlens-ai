"""Collects every v1 endpoint. New feature routers are registered here."""

from fastapi import APIRouter, Depends

from app.api.v1 import cvs, health, jobs
from app.core.security import require_api_key

api_router = APIRouter()
# The health check stays open so the hosting platform can probe it; it returns no candidate data.
api_router.include_router(health.router)
api_router.include_router(cvs.router, dependencies=[Depends(require_api_key)])
api_router.include_router(jobs.router, dependencies=[Depends(require_api_key)])
