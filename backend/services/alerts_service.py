from backend.database.db import SessionLocal
from backend.database.models import Alert
import datetime

def create_alert(disaster_type, location, severity, population_at_risk):
    db = SessionLocal()
    alert = Alert(
        disaster_type=disaster_type,
        location=location,
        severity=severity,
        population_at_risk=population_at_risk,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    db.close()
    return alert.id

def get_active_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).all()
    db.close()
    return [{"id": a.id, "disaster_type": a.disaster_type, "location": a.location,
             "severity": a.severity, "population_at_risk": a.population_at_risk,
             "timestamp": a.timestamp} for a in alerts]
