from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import datetime

router = APIRouter()

# Global cache simulation with real-world coordinates for testing
PREDICTION_CACHE = {
    "stats": {
        "ai_accuracy_percent": 92.5,
        "total_affected_population_M": 1.9,
        "active_alert_count": 5,
        "critical_zone_count": 3
    },
    "heatmap": [
        # LIVE DATA (T+0)
        {"lat": 26.1445, "lng": 91.7362, "intensity": 0.85, "type": "flood", "hourOffset": 0},
        {"lat": 28.6139, "lng": 77.2090, "intensity": 0.90, "type": "heatwave", "hourOffset": 0},
        {"lat": 30.0668, "lng": 79.0193, "intensity": 0.70, "type": "landslide", "hourOffset": 0},
        # FORECAST DATA (T+12 to T+24)
        {"lat": 20.2961, "lng": 85.8245, "intensity": 0.65, "type": "cyclone", "hourOffset": 12},
        {"lat": 34.0837, "lng": 74.7973, "intensity": 0.45, "type": "earthquake", "hourOffset": 24}
    ],
    "activeThreats": ["flood", "cyclone", "earthquake", "landslide", "heatwave"],
    "last_updated": datetime.datetime.now().strftime("%H:%M:%S")
}

@router.get("/stats")
async def get_all_predictions():
    """Unified endpoint for the dashboard stats and heatmap"""
    return PREDICTION_CACHE