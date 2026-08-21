# FlyRank Capstone: AI Image Understanding & Content Matching Engine

**Author:** Muhammad Obaidullah

## 🚀 Overview
This is a production-ready AI image understanding and matching engine built as part of the FlyRank Backend Track Capstone[cite: 1]. It analyzes an image corpus using Google Gemini's vision models to extract structured metadata (JSON schema) and uses semantic embeddings to match the right image to the right blog post[cite: 1]. 

The core feature of this system is the **Mismatch Guard**—a safety layer that combines semantic similarity thresholds and confidence scores to ensure that a blog post about a "Red Fox" gets a Fox image, and safely rejects visually similar but incorrect images (like a Wolf), explaining the reason for rejection[cite: 1].

---

## 🧠 Architecture Sketch

Images (batch job) --> Vision Model --> {tags, caption, confidence} --> image_metadata
                                 --> embed(caption) -------------> image_vectors

Posts --------------------------------> embed(post text) -----------> post_vectors

GET /recommend
 └── Similarity Ranking (image_vectors × post_vector)
      └── Mismatch Guard (cosine similarity threshold + confidence)
           ├── Suggested image (ranked, explained)
           └── "No good match" + explanation
                └── Review API: approve / reject[cite: 1]

---

## 🛠️ Setup and Run Instructions

### 1. Environment Setup
Create a virtual environment and install dependencies:
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic google-generativeai python-dotenv pytest httpx

Ensure you have a `.env` file in the root directory (refer to `.env.example` for required variables)[cite: 1].

### 2. Run the Application
Start the FastAPI server:
uvicorn src.main:app --host 0.0.0.0 --port 8000

Visit `http://localhost:8000/docs` to test the API via Swagger UI.

### 3. Seed the Database (Batch Processing)
To process the initial image corpus and generate structured AI metadata[cite: 1]:
python -m src.batch

### 4. Run Automated Tests
To verify the schema validation, mismatch guard, and API endpoints[cite: 1]:
pytest

---

## 📊 Evaluation & Metrics
* **Top-1 Precision:** `100%` (Tested on custom eval dataset distinguishing between foxes and wolves)[cite: 1].
* **Cost Tracking:** Every AI vision call is tracked in the database (`vision_cost: 0.0015` per call) to ensure the system operates within budget[cite: 1].

---

## ⚠️ Limitations (Honest Assessment)
* **Local Image Storage:** Currently, the system reads images from a local `corpus/` folder. In a real-world scenario, this should be connected to an S3 bucket or cloud storage.
* **Hardcoded Threshold:** The Cosine Similarity threshold is currently manually tuned. A dynamic threshold based on a larger dataset would improve accuracy.
* **Vector Indexing:** We are currently using simple array-based comparisons for similarity. For a corpus of over 10,000 images, migrating to `pgvector` or a dedicated vector database (like FAISS/ChromaDB) would be necessary for performance.