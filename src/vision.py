import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from src.schemas import ImageMetadataSchema

# Secrets load karein
load_dotenv()

# Gemini configure karein
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Flash model initialize karein
model = genai.GenerativeModel('gemini-3.6-flash')

def analyze_image(image_path: str):
    """Image ko parh kar Pydantic schema ke mutabiq JSON nikaalta hai."""
    
    # Image ko bytes mein read karna
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    # Gemini ko file bhejne ke liye format
    image_part = {
        "mime_type": "image/jpeg",
        "data": image_bytes
    }
    
    prompt = "Analyze this image and provide the metadata exactly matching the required JSON schema."
    
    try:
        # API call with strict structured output config
        response = model.generate_content(
            [image_part, prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ImageMetadataSchema,
                temperature=0.2 # Kam temperature taake AI bilkul to-the-point baat kare
            )
        )
        
        # JSON text ko Python dictionary mein convert karna
        metadata = json.loads(response.text)
        return metadata
    
    except Exception as e:
        return {"error": str(e)}