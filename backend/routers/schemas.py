from pydantic import BaseModel
from typing import Optional, Dict, Any

class PredictionResponse(BaseModel):
    disaster_type: str
    prediction: Optional[Any]
    probability: Optional[Any]
    severity: Optional[str]
    timestamp: Optional[str]

class AlertCreate(BaseModel):
    disaster_type: str
    latitude: float
    longitude: float
    severity: str
    details: Optional[Dict] = None
    population: Optional[int] = None

