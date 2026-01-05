# backend/database/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Your PostgreSQL connection string (Ensure this is correct)
# NOTE: The driver is changed from '+asyncpg' to standard for synchronous FastAPI dependency
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Diya30@localhost:5432/disasters")

# Replace the async driver for the synchronous engine connection
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() # Define Base here for models

def get_db():
    """Dependency to yield a new database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()