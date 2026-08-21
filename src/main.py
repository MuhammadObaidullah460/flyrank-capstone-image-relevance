from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from src.models import Base  # <-- Naya import

# .env file se secrets load karein
load_dotenv()

app = FastAPI(title="AI Image Matching Engine")

# Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database mein tables create karna
Base.metadata.create_all(bind=engine)  # <-- Yeh line tables generate karegi

@app.get("/")
def read_root():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "Connected 🟢 Tables Created!"
    except Exception as e:
        db_status = f"Disconnected 🔴 ({e})"

    return {
        "message": "Capstone Engine is running!", 
        "database": db_status
    }