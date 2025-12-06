from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine with SQLite configuration
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # For SQLite
)

# Create session factory for database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

# Dependency function to get database session
def get_db():
    """Get database session for API endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        # Close session after request
        db.close()

