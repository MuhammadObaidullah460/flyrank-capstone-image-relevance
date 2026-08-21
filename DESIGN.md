# Capstone Design Document: AI Image Understanding & Content Matching Engine

## 1. Problem Statement
The goal is to build an AI-powered system that automatically processes an image library to extract structured metadata (tags and captions), and semantically matches the most relevant image to a given blog post. Crucially, the system will feature a "Mismatch Guard" to safely reject incorrect recommendations (e.g., suggesting a wolf for a fox article) and provide an explanation when no confident match is found.

## 2. Layer Sketch (Architecture)
* **Framework:** Python with FastAPI for building robust, layered HTTP endpoints.
* **Database:** PostgreSQL for persisting images, embeddings, posts, and review logs.
* **AI Provider:** Gemini Flash API (Free Tier) for both vision understanding (structured JSON output) and text/image embeddings.
* **Processing:** Background batch processing for image ingestion, preventing long-running AI calls from blocking the main request thread.

## 3. Data Model (Image Metadata Schema)
The vision model will output structured, schema-validated JSON for each image:
* `subject` (string): The primary entity in the image (e.g., "red fox").
* `category` (string): The general classification (e.g., "animal").
* `attributes` (array of strings): Key visual traits (e.g., ["orange fur", "forest", "wild"]).
* `caption` (string): A short, descriptive summary for embedding generation.
* `confidence` (float): The AI's certainty score (0.0 to 1.0). Low-confidence results will be flagged.

## 4. API Surface
* `POST /images/batch`: Triggers the background job to process raw images, generate tags/embeddings, and track API costs.
* `GET /posts/{id}/images`: Semantic matching endpoint. Runs the vector similarity search, passes candidates through the Mismatch Guard, and returns ranked suggestions (or a confident rejection).
* `POST /suggestions/{id}/review`: A human-in-the-loop endpoint to approve or reject the AI's suggested image pairing.

## 5. Explicit Non-Goal
This project will focus entirely on backend architecture, AI safety layers, and API endpoints. **Building a graphical User Interface (UI) or a frontend application is an explicit non-goal.** The review workflow will be handled purely via validated API endpoints.