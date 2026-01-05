# backend/routers/alerts.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

# --- Imports for Database Integration ---
from ..database import crud
from ..database.db import get_db 

router = APIRouter()

# --- Pydantic Schema for Alert Response ---
class Alert(BaseModel):
    id: int
    disaster_type: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[str] = None
    population_at_risk: Optional[int] = None
    timestamp: Optional[datetime] = None

class ActiveAlertsResponse(BaseModel):
    status: str
    alerts: List[Alert]

# --- Router with DB Dependency ---
@router.get("/active_alerts", response_model=ActiveAlertsResponse)
def get_active_alerts(db: Session = Depends(get_db)):
    """
    Fetches all active disaster alerts from the database, filters, and formats them.
    This replaces the mock data.
    """
    
    # 1. Fetch data directly from the CRUD layer
    try:
        raw_alerts = crud.get_active_alerts_from_db(db)
    except Exception:
        # Re-raise the exception to show the DB error in the console
        raise 
        
    # 2. Final check for nulls (safeguard)
    clean_alerts = [
        alert for alert in raw_alerts 
        if alert.get('disaster_type') is not None and alert.get('timestamp') is not None
    ]
    
    return {"status": "success", "alerts": clean_alerts}