import os
import google.generativeai as genai
from dotenv import load_dotenv

# Secrets load karein
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str):
    """Text (caption ya blog post) ko vector (numbers ki list) mein convert karta hai."""
    try:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="semantic_similarity"
        )
        return result['embedding']
    
    except Exception as e:
        print(f"Embedding error: {e}")
        return None