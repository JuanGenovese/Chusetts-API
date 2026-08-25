from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db



router = APIRouter(prefix="/caja", tags=["Caja"])


@router.get("/status")
def get_cash_session_status():
    """Get active cash shift/session status."""
    return {"message": "Caja domain scaffold ready"}

