import os
from src.main import SessionLocal
from src.models import ImageRecord
from src.vision import analyze_image

def process_images_in_bulk(folder_path="corpus"):
    db = SessionLocal()
    try:
        # Folder ki saari images par loop chalayein
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(folder_path, filename)
                print(f"\nProcessing {filename}...")

                # Check karein agar image pehle se database mein hai toh skip karein (Idempotency)
                existing = db.query(ImageRecord).filter(ImageRecord.filename == filename).first()
                if existing:
                    print(f"Skipping {filename} - already in database.")
                    continue

                # AI se data mangwayein
                ai_data = analyze_image(file_path)

                if "error" in ai_data:
                    print(f"Error processing {filename}: {ai_data['error']}")
                    continue

                # Database mein save karne ke liye record banayein
                new_record = ImageRecord(
                    filename=filename,
                    subject=ai_data.get("subject"),
                    category=ai_data.get("category"),
                    attributes=ai_data.get("attributes"),
                    caption=ai_data.get("caption"),
                    confidence=ai_data.get("confidence"),
                    status="processed",
                    vision_cost=0.0015  # Requirement: Cost tracking per call
                )
                
                # Agar confidence kam ho toh status flag kar dein
                if new_record.confidence < 0.70:
                    new_record.status = "flagged"
                    print("⚠️ Low confidence detected, flagging image.")

                db.add(new_record)
                db.commit()
                print(f"✅ Successfully saved {filename} to database!")
                
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting Batch Vision Processing...")
    process_images_in_bulk()