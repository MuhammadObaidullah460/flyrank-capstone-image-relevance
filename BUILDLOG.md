# AI Usage Build Log

**Where AI helped:**
* **Boilerplate & Infrastructure:** Used AI to quickly scaffold the FastAPI application structure and SQLAlchemy database models for images, posts, and match reviews.
* **Mathematical Logic:** Used AI to write the pure Python Cosine Similarity function for embedding comparisons without heavy external dependencies.
* **Debugging & Models:** Helped resolve API model naming adjustments for Google Gemini vision and embedding models.

**Where AI was wrong and what I changed:**
* **Deprecation Warnings:** AI initially suggested the older `google.generativeai` library syntax. I managed the library versions and warnings manually to fit current standards.
* **Test Database State:** The AI generated a review test that failed due to missing foreign key constraints. I manually added database record seeding inside `test_main.py` so `pytest` runs smoothly.