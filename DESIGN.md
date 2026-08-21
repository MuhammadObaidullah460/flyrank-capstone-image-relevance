# Capstone Design Document: AI Image Understanding & Content Matching Engine

## 1. Problem Statement
Managing large image libraries for content publishing manually is inefficient. Content management systems often mismatch images and blog posts based on weak keyword matching (e.g., placing a wolf image on a red fox article), leading to poor content quality.

## 2. Data Model & Architecture
* **Images Table:** Stores filename, AI-extracted subject, category, attributes, caption, confidence score, status, and vision cost.
* **Posts Table:** Stores blog post text content.
* **Match Reviews Table:** Tracks human-in-the-loop review trails (approvals/rejections and reasons).
* **Pipeline:** Two parallel streams (image captions and post text) converted into vector embeddings, compared via Cosine Similarity, and filtered through a Mismatch Guard.

## 3. API Surface
* `GET /`: Health check and database connectivity status.
* `POST /recommend`: Accepts blog text, computes semantic similarity against processed images, and returns the best matching image with a mismatch guard evaluation.
* `POST /review`: Human-in-the-loop review endpoint to approve or reject a suggested image pairing.

## 4. Explicit Non-Goals
* Building a full-scale cloud image hosting platform or CDN.
* Developing a complex multi-page frontend UI (backend APIs and evaluation scripts are prioritized).