from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from src.models import Base, ImageRecord
from src.matcher import evaluate_match

# Secrets load karein
load_dotenv()

app = FastAPI(title="AI Image Matching Engine")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tables create karna
Base.metadata.create_all(bind=engine)

# Request Schema
class BlogRequest(BaseModel):
    blog_text: str

@app.get("/")
def read_root():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "Connected 🟢 Tables Created!"
    except Exception as e:
        db_status = f"Disconnected 🔴 ({e})"
    return {"message": "Capstone Engine is running!", "database": db_status}

@app.post("/recommend")
def recommend_image(request: BlogRequest):
    """Blog text leta hai aur sab se behtareen image match nikaal kar deta hai."""
    db = SessionLocal()
    try:
        # Database se sirf processed images layein
        images = db.query(ImageRecord).filter(ImageRecord.status == "processed").all()
        
        if not images:
            raise HTTPException(status_code=404, detail="No processed images found in database.")

        best_match = None
        highest_score = 0.0

        # Har image ke caption ko blog text se compare karein
        for img in images:
            score = evaluate_match(request.blog_text, img.caption)
            if score > highest_score:
                highest_score = score
                best_match = img

        if best_match:
            return {
                "recommended_image": best_match.filename,
                "match_score": round(highest_score, 2),
                "metadata": {
                    "subject": best_match.subject,
                    "caption": best_match.caption
                }
            }
        
        return {"message": "No suitable match found."}
    finally:
        db.close()

class ReviewRequest(BaseModel):
    post_id: int
    image_id: int
    is_approved: bool
    reason: str = None

@app.post("/review")
def review_match(request: ReviewRequest):
    """Human-in-the-loop review API: Approves or rejects a suggested match."""
    from src.models import MatchReview
    db = SessionLocal()
    try:
        new_review = MatchReview(
            post_id=request.post_id,
            image_id=request.image_id,
            is_approved=request.is_approved,
            reason=request.reason
        )
        db.add(new_review)
        db.commit()
        return {
            "message": "Review saved successfully!", 
            "status": "Approved" if request.is_approved else "Rejected"
        }
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()