# backend/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from .config import PREDICTION_CACHE
from .services.data_ingestion_service import run_predictions_and_update_cache

# --- Scheduler Setup ---
scheduler = AsyncIOScheduler()

def start_scheduler():
    """Starts the background job to run predictions periodically."""
    print("Initializing APScheduler...")

    # Schedule prediction to run every 15 minutes
    scheduler.add_job(
        run_predictions_and_update_cache, 
        'interval', 
        minutes=15, 
        id='prediction_job',
        max_instances=1
    )
    
    # Run once immediately on startup to populate the cache
    scheduler.add_job(
        run_predictions_and_update_cache, 
        'date', 
        run_date=datetime.now(), 
        id='initial_run',
        max_instances=1
    )
    
    scheduler.start()
    print("APScheduler started. Predictions are running on a 15-minute interval.")