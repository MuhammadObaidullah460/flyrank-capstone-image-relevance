from sqlalchemy import Column, Integer, String, Float, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ImageRecord(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    subject = Column(String, nullable=True)
    category = Column(String, nullable=True)
    attributes = Column(JSON, nullable=True)
    caption = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    status = Column(String, default="pending")
    vision_cost = Column(Float, default=0.0)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

class MatchReview(Base):
    __tablename__ = "match_reviews"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    image_id = Column(Integer, ForeignKey("images.id"))
    is_approved = Column(Boolean, nullable=False)
    reason = Column(Text, nullable=True)