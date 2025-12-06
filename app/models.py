# Database models for mental health application
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

# ===== DISORDER MODEL =====
# Stores information about mental health conditions
class Disorder(Base):
    __tablename__ = "disorders"
    
    # Primary key for the disorder
    id = Column(Integer, primary_key=True, index=True)
    
    # Disorder information
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    symptoms = Column(Text)
    
    # Timestamp when record was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ===== REMEDY MODEL =====
# Stores treatment options for disorders
class Remedy(Base):
    __tablename__ = "remedies"
    
    # Primary key for the remedy
    id = Column(Integer, primary_key=True, index=True)
    
    # Link to the disorder this remedy treats
    disorder_id = Column(Integer, ForeignKey("disorders.id"), nullable=False)
    
    # Remedy information
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String)  # Type: therapy, medication, or lifestyle
    
    # Timestamp when record was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())
