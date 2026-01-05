from fastapi import APIRouter
from backend.services.zones_service import get_critical_zones

router = APIRouter()

@router.get("/critical_zones/{disaster_type}")
def critical_zones(disaster_type: str):
    return {"status": "success", "geojson": get_critical_zones(disaster_type)}
