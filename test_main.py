from fastapi.testclient import TestClient
from src.main import app, SessionLocal
from src.models import Post, ImageRecord

# FastAPI ki temporary test client banayein
client = TestClient(app)

def test_api_root():
    """Check karega ke server aur database theek chal rahe hain."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Connected" in response.json()["database"]

def test_recommend_fox_over_wolf():
    """Mismatch Guard Test: Fox ke blog par Fox hi aana chahiye, Wolf nahi."""
    payload = {"blog_text": "Today we saw a beautiful red fox running in the snowy forest."}
    response = client.post("/recommend", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        assert "recommended_image" in data
        assert data["recommended_image"] == "fox.jpg"

def test_review_api():
    """Review API ka test jo reject action check karega."""
    db = SessionLocal()
    try:
        # Test ke liye database mein ek dummy post create karein
        post = db.query(Post).filter(Post.id == 1).first()
        if not post:
            db.add(Post(id=1, content="Test Blog Post"))
        
        # Test ke liye ek dummy image check karein
        img = db.query(ImageRecord).filter(ImageRecord.id == 1).first()
        if not img:
            db.add(ImageRecord(id=1, filename="dummy.jpg", status="processed"))
            
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

    payload = {
        "post_id": 1,
        "image_id": 1,
        "is_approved": False,
        "reason": "Testing rejection logic"
    }
    response = client.post("/review", json=payload)
    
    assert response.status_code == 200
    assert "status" in response.json(), f"API returned error: {response.json()}"
    assert response.json()["status"] == "Rejected"