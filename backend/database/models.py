# backend/database/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base # Import Base from your db.py

class DisasterEvent(Base):
    __tablename__ = "disaster_events"
    
    # Core Fields
    id = Column(Integer, primary_key=True, index=True)
    disaster_type = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Location/Population (These fields MUST be in the database schema)
    location_name = Column(String, nullable=True) 
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status
    population_at_risk = Column(Integer, default=0) 
    alert_sent = Column(Integer, default=1) # 1=Active, 0=Inactive/Resolved