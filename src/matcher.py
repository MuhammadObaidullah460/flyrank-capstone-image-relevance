import math
from src.embeddings import get_embedding

def cosine_similarity(v1, v2):
    """Do vectors ke darmiyan similarity score calculate karta hai."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a * a for a in v1))
    magnitude2 = math.sqrt(sum(b * b for b in v2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def evaluate_match(blog_text: str, image_caption: str):
    """Blog post aur image caption ki embeddings mangwa kar match score nikaalta hai."""
    
    blog_vec = get_embedding(blog_text)
    caption_vec = get_embedding(image_caption)
    
    if not blog_vec or not caption_vec:
        print("Error: Embeddings generate nahi ho sakeen.")
        return 0.0
        
    score = cosine_similarity(blog_vec, caption_vec)
    return score