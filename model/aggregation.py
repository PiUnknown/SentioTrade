import numpy as np

def aggregate_sentiment(results: list[dict]) -> dict:
    if not results:
        return {"sentiment": "neutral", "confidence": 0.0, "post_count": 0}

    positive_scores = []
    negative_scores = []
    neutral_scores = []

    for r in results:
        label = r["label"].lower()
        score = r["score"]

        if label == "positive":
            positive_scores.append(score)
        elif label == "negative":
            negative_scores.append(score)
        else:
            neutral_scores.append(score)

    summary = {
        "positive_posts": len(positive_scores),
        "negative_posts": len(negative_scores),
        "neutral_posts": len(neutral_scores),
        "avg_positive_confidence": round(float(np.mean(positive_scores)), 3) if positive_scores else 0.0,
        "avg_negative_confidence": round(float(np.mean(negative_scores)), 3) if negative_scores else 0.0,
        "post_count": len(results)
    }

    counts = {
        "positive": len(positive_scores),
        "negative": len(negative_scores),
        "neutral": len(neutral_scores)
    }
    summary["overall_sentiment"] = max(counts, key=counts.get)

    return summary