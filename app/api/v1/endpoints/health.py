# app/api/v1/endpoints/quotes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.health import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def get_health():
    return {"status": "ok", "message": "Service is running"}