"""Collects every v1 endpoint. New feature routers are registered here."""

from fastapi import APIRouter

from app.api.v1 import cvs, health, jobs

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(cvs.router)
api_router.include_router(jobs.router)
