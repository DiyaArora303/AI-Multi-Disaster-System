# create_tables.py

# Import the necessary components
from backend.database.db import engine, Base
from backend.database import models # Ensures models are loaded for Base.metadata.create_all

print("Attempting to drop and create all tables...")

try:
    # 1. Drop all existing tables (DANGER: Deletes all old data!)
    Base.metadata.drop_all(bind=engine)
    print("Existing tables dropped successfully.")

    # 2. Create all tables defined in Base (loads the new schema)
    Base.metadata.create_all(bind=engine)
    print("New tables (disaster_events) created successfully.")
    
except Exception as e:
    print(f"CRITICAL DB ERROR: Could not connect or run schema migration: {e}")
    
print("Database schema synchronization complete.")