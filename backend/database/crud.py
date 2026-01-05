# backend/database/crud.py

from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from typing import List, Dict, Any

# =======================================================================
# READ (Function called by the alerts router)
# =======================================================================

def get_active_alerts_from_db(db: Session, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Fetches active alerts from the DB and formats them for the frontend router.
    """
    
    # Query: Get events that are active (alert_sent=1) and sort by time.
    events = db.query(models.DisasterEvent) \
        .filter(models.DisasterEvent.alert_sent == 1) \
        .order_by(models.DisasterEvent.timestamp.desc()) \
        .limit(limit) \
        .all()
        
    # Format results to match the Pydantic schema structure expected by the router
    formatted_alerts = []
    for event in events:
        # Combine name and coordinates into the single 'location' string required by the frontend
        # This fixes the display issue on the map component
        location_str = f"{event.location_name}, {event.latitude}, {event.longitude}"
        
        formatted_alerts.append({
            "id": event.id,
            "disaster_type": event.disaster_type,
            "location": location_str, 
            "severity": event.severity,
            "population_at_risk": event.population_at_risk,
            "timestamp": event.timestamp.isoformat() if event.timestamp else None,
        })
        
    return formatted_alerts

# Function to create an event (keeping for completeness)
def create_disaster_event(db: Session, disaster_type: str, location_name: str, 
                         lat: float, lon: float, severity: str, population: int, 
                         alert_sent: bool = True):
    
    event = models.DisasterEvent(
        disaster_type=disaster_type,
        location_name=location_name,
        latitude=lat,
        longitude=lon,
        severity=severity,
        population_at_risk=population,
        alert_sent=alert_sent,
        timestamp=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event