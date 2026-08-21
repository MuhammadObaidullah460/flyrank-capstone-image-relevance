from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env file se secrets load karein
load_dotenv()

# FastAPI app initialize karein
app = FastAPI(title="AI Image Matching Engine")

# Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/")
def read_root():
    try:
        # Database connection test karna
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "Connected 🟢"
    except Exception as e:
        db_status = f"Disconnected 🔴 ({e})"

    return {
        "message": "Capstone Engine is running!", 
        "database": db_status
    }