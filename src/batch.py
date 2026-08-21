import os
import time
from src.main import SessionLocal
from src.models import ImageRecord
from src.vision import analyze_image

def process_images_in_bulk(folder_path="corpus"):
    db = SessionLocal()
    max_retries = 3  # Retry limit set karna
    
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(folder_path, filename)
                print(f"\nProcessing {filename}...")

                # Idempotency: Check karein agar image pehle se hai
                existing = db.query(ImageRecord).filter(ImageRecord.filename == filename).first()
                if existing:
                    print(f"Skipping {filename} - already in database.")
                    continue

                ai_data = None
                
                # Retry Logic: Agar API fail ho toh 3 dafa koshish kare
                for attempt in range(max_retries):
                    ai_data = analyze_image(file_path)
                    if "error" not in ai_data:
                        break  # Agar error nahi aya toh loop se bahar aa jayein
                    
                    print(f"⚠️ Attempt {attempt + 1} failed for {filename}: {ai_data['error']}")
                    time.sleep(2)  # 2 second ruk kar dobara try karein

                if ai_data is None or "error" in ai_data:
                    print(f"❌ Failed to process {filename} after {max_retries} attempts.")
                    continue

                new_record = ImageRecord(
                    filename=filename,
                    subject=ai_data.get("subject"),
                    category=ai_data.get("category"),
                    attributes=ai_data.get("attributes"),
                    caption=ai_data.get("caption"),
                    confidence=ai_data.get("confidence"),
                    status="processed",
                    vision_cost=0.0015
                )
                
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
    print("Starting Batch Vision Processing with Retries...")
    process_images_in_bulk()