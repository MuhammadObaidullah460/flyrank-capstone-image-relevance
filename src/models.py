from sqlalchemy import Column, Integer, String, Float, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ImageRecord(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    
    # AI Vision Output Fields
    subject = Column(String, nullable=True)
    category = Column(String, nullable=True)
    attributes = Column(JSON, nullable=True) # Array of strings ko JSON mein save karenge
    caption = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    
    # Processing & Cost Tracking
    status = Column(String, default="pending") # 'pending', 'processed', ya 'flagged'
    vision_cost = Column(Float, default=0.0)