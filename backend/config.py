# backend/config.py

import os
from datetime import datetime
from typing import Dict, List, Union, Any

# --- Disaster Types ---
DISASTER_TYPES = ['cyclone', 'flood', 'earthquake', 'landslide', 'heatwave', 'drought']

# --- File Paths ---
MODEL_PATH = os.path.join(os.getcwd(), 'models')

# --- Database Placeholder ---
DATABASE_URL = "sqlite:///./disaster_alerts.db"

# Global Cache Initialization
# This structure must match the React frontend's expectations
PREDICTION_CACHE: Dict[str, Any] = {
    "last_updated": datetime.now().isoformat(),
    "stats": {
        "ai_accuracy_percent": 92.5,
        "total_affected_population_M": 0.0,
        "active_alert_count": 0,
        "critical_zone_count": 0,
    }
}

# Initialize empty lists for each disaster type
for dtype in DISASTER_TYPES:
    PREDICTION_CACHE[dtype] = []

print("--- [CONFIG] PREDICTION_CACHE Initialized successfully ---")