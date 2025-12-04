# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

# Disorder model - stores mental health conditions
class Disorder(Base):
    _tablename_ = "disorders"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Disorder details
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    symptoms = Column(Text)
    
 Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Remedy model - stores treatment options
class Remedy(Base):
    _tablename_ = "remedies"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to disorder
    disorder_id = Column(Integer, ForeignKey("disorders.id"), nullable=False)
    
    # Remedy details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String)  # therapy, medication, lifestyle
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())