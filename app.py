from fastapi import FastAPI, HTTPException
from scraper.reddit_scraper import fetch_posts
from model.main_model import analyze_sentiment
from model.aggregation import aggregate_sentiment
from fastapi.responses import FileResponse

app = FastAPI(title="SentioTrade", description="Stock sentiment analysis from Reddit")

@app.get("/")
def serve_ui():
    return FileResponse("index.html")


@app.get("/sentiment/{ticker}")
def get_sentiment(ticker: str, limit: int = 50):
    ticker = ticker.upper()
    
    posts = fetch_posts(ticker, limit=limit)
    
    if not posts:
        raise HTTPException(
            status_code=404,
            detail=f"No posts found for {ticker}"
        )
    
    sentiment_results = analyze_sentiment(posts)
    summary = aggregate_sentiment(sentiment_results)
    
    return {
        "ticker": ticker,
        "summary": summary
    }   