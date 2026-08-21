from pydantic import BaseModel, Field
from typing import List

class ImageMetadataSchema(BaseModel):
    subject: str = Field(..., description="The primary entity in the image (e.g., 'red fox', 'gray wolf')")
    category: str = Field(..., description="The general classification (e.g., 'animal', 'landscape')")
    attributes: List[str] = Field(..., description="Key visual traits (e.g., ['orange fur', 'wild', 'forest'])")
    caption: str = Field(..., description="A short, descriptive summary for the image")
    confidence: float = Field(..., description="The AI's certainty score from 0.0 to 1.0")