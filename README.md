# SentioTrade 📈
### Real-time Stock Sentiment Analysis via Reddit · FinBERT · FastAPI · Docker

> Built end-to-end by a 2nd year B.Tech student as a demonstration of production-grade ML system design — from raw data ingestion to a containerized, deployable API with a live frontend.

---

## What This Project Does

SentioTrade ingests live Reddit discussions from finance communities (r/wallstreetbets, r/stocks, r/investing, r/stockmarket), runs them through **FinBERT** — a BERT model fine-tuned on financial language — and returns a structured sentiment summary for any queried stock ticker.

A user queries `$TSLA` → the system scrapes Reddit → FinBERT scores each post → aggregation produces a final sentiment verdict → FastAPI returns a JSON response → the frontend renders it in real time.

---

## Why This Project Exists (The Problem)

Most sentiment tools use general-purpose NLP models trained on generic English text. These models fail on financial language because:

- **Domain-specific jargon** ("puts printing", "short squeeze", "going to the moon") is semantically invisible to general models
- **Inverted sentiment** — "TSLA down 8%" is negative for longs, positive for shorts
- **Pervasive sarcasm** on r/wallstreetbets breaks naive positive/negative classification

SentioTrade uses **FinBERT (ProsusAI)**, trained specifically on financial corpora, to handle these edge cases correctly.

---

## System Architecture

```
User Query ($TSLA)
        │
        ▼
┌─────────────────┐
│   FastAPI Layer  │  ← Receives query, orchestrates pipeline
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reddit Scraper  │  ← PRAW · Searches 4 subreddits · 2 query variants per ticker
│  (scraper/)      │    returns up to 400 posts per request
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FinBERT Model   │  ← HuggingFace Transformers · Per-post classification
│  (model/)        │    Output: Positive / Negative / Neutral + confidence score
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Aggregation    │  ← NumPy · Weighted averaging · Overall sentiment verdict
│  (model/)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Response   │  ← Structured output with post counts + confidence metrics
└─────────────────┘
```

---

## Key Engineering Decisions

### Why FinBERT over VADER or TextBlob?
General sentiment tools like VADER were trained on social media but not financial language. FinBERT was fine-tuned on analyst reports and financial news — it understands that "bearish momentum" is negative even though "momentum" is positive in general English.

### Why FastAPI over Flask?
FastAPI provides native async support (critical for concurrent Reddit scraping), automatic data validation via Pydantic, and auto-generated `/docs` interface — all without additional configuration. Flask requires manual implementation of all three.

### Why Docker?
Eliminates environment-specific failures. FinBERT + PyTorch dependencies are notoriously version-sensitive. Docker ensures the model loads identically across any machine — local, staging, or cloud.

### Why separate Aggregation from FinBERT?
Single responsibility principle. FinBERT's job is per-post classification. Aggregation's job is combining 400 scores into a human-readable signal. Keeping them separate makes each independently testable and replaceable.

### Mock Data Strategy
Reddit API credentials require approval time. Rather than blocking development on an external dependency, the scraper was built with a mock data layer that mirrors the real API's return signature. When credentials are available, swapping in the real scraper requires changing one file.

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| NLP Model | FinBERT (ProsusAI) | Financial domain fine-tuning |
| ML Framework | HuggingFace Transformers + PyTorch | Industry standard for transformer inference |
| Data Source | Reddit via PRAW | Largest retail investor sentiment signal |
| API Framework | FastAPI | Async, typed, self-documenting |
| Aggregation | NumPy | Efficient numerical operations |
| Containerization | Docker | Reproducible deployment |
| Frontend | Vanilla JS + CSS | Zero-dependency, terminal-aesthetic UI |

---

## Project Structure

```
SentioTrade/
│
├── scraper/
│   ├── __init__.py
│   └── reddit_scraper.py      # PRAW client + multi-subreddit search
│
├── model/
│   ├── __init__.py
│   ├── main_model.py          # FinBERT pipeline (loaded once at startup)
│   └── aggregation.py         # Score aggregation + sentiment verdict
│
├── app.py                     # FastAPI app + endpoint definitions
├── index.html                 # Frontend UI (served directly by FastAPI)
├── Dockerfile                 # CPU-optimized container build
├── .dockerignore              # Excludes venv, credentials, pycache
├── requirements.txt           # Pinned dependencies
└── .env                       # Credentials (gitignored)
```

---

## API Response Example

```json
GET /sentiment/TSLA

{
  "ticker": "TSLA",
  "summary": {
    "positive_posts": 6,
    "negative_posts": 3,
    "neutral_posts": 1,
    "avg_positive_confidence": 0.891,
    "avg_negative_confidence": 0.743,
    "post_count": 10,
    "overall_sentiment": "positive"
  }
}
```

---

## Running Locally

### Prerequisites
- Python 3.10+
- Docker Desktop
- Reddit API credentials (see below)

### Option 1 — Docker (Recommended)

```bash
git clone https://github.com/PiUnknown/SentioTrade.git
cd SentioTrade

# Add your Reddit credentials
cp .env.example .env
# Edit .env with your REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET

# Build and run
docker build -t sentiotrade .
docker run -p 8000:8000 sentiotrade
```

Visit `http://localhost:8000` for the UI or `http://localhost:8000/docs` for the API.

### Option 2 — Local Python

```bash
git clone https://github.com/PiUnknown/SentioTrade.git
cd SentioTrade

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
uvicorn app:app --reload
```

### Reddit API Setup

1. Go to `https://www.reddit.com/prefs/apps`
2. Create a new app → type: **script**
3. Copy `client_id` and `client_secret` into `.env`:

```
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
```

> Without credentials, the system runs on mock data and still demonstrates the full NLP pipeline.

---

## Limitations & Honest Assessment

This project is transparent about what it can and cannot claim:

- **Sentiment ≠ price prediction.** SentioTrade measures what people are *saying*, not what the market will *do*. These are correlated but not causal.
- **Reddit is noisy.** r/wallstreetbets is particularly susceptible to coordinated posts, meme stocks, and irony. The model handles sarcasm better than VADER but is not immune.
- **Snapshot, not streaming.** Each query is a point-in-time scrape. A production system would require a scheduled pipeline with historical trending.

These limitations are intentional to document — understanding where a model fails is as important as knowing where it works.

---

## Author

**Om** · B.Tech 2nd Year · ML/AI Engineering  
[GitHub](https://github.com/PiUnknown) · [LinkedIn](https://www.linkedin.com/in/omkumarjha043/)

> Previous work includes geospatial ML pipelines (Indian Navy internship), RAG-based retrieval systems (QueryForge), CV pipelines (VisionSynth), and agentic workflow experiments.