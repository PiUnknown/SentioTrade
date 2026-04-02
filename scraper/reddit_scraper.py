import os
from dotenv import load_dotenv

load_dotenv()

def fetch_posts(ticker: str, limit: int = 50) -> list[str]:
    # MOCK DATA - replace with real PRAW scraper once Reddit credentials are ready
    mock_posts = [
        f"{ticker} is looking incredibly bullish right now, strong buy signal",
        f"I just doubled my position in {ticker}, fundamentals are solid",
        f"{ticker} earnings beat expectations, stock likely to surge",
        f"Dumping all my {ticker} shares, this company is finished",
        f"{ticker} is overvalued and the bubble is about to burst",
        f"Not sure about {ticker}, mixed signals from the market today",
        f"Long term hold on {ticker}, not worried about short term dips",
        f"{ticker} down 8% today, panic selling is overdone in my opinion",
        f"Institutional investors are loading up on {ticker} quietly",
        f"{ticker} puts printing today, bears are winning this week",
    ]
    return mock_posts