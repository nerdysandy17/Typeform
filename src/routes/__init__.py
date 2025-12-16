"""Init."""

from fastapi import APIRouter

from src.routes import health

root_router = APIRouter()
root_router.include_router(health.router)
