from fastapi import APIRouter
from app.api.v1.endpoints import document, health

api_router = APIRouter()
api_router.include_router(document.router, prefix="/documents", tags=["document management"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
