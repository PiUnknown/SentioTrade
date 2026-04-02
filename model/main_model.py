from transformers import pipeline

def load_model():
    return pipeline(
        "text-classification",
        model="ProsusAI/finbert",
        tokenizer="ProsusAI/finbert"
    )

finbert = load_model()

def analyze_sentiment(texts: list[str]) -> list[dict]:
    results = []
    for text in texts:
        # FinBERT has a 512 token limit, truncate to be safe
        truncated = text[:512]
        result = finbert(truncated)[0]
        results.append({
            "text": truncated,
            "label": result["label"],
            "score": result["score"]
        })
    return results