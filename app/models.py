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
    
