"""Sentiment scorer wrapping a HuggingFace classifier."""
import os
from functools import lru_cache
from transformers import pipeline

LABELS = {"negative": -1, "neutral": 0, "positive": 1}


@lru_cache(maxsize=1)
def _model():
    name = os.getenv("SENTIMENT_MODEL", "cardiffnlp/twitter-roberta-base-sentiment-latest")
    return pipeline("sentiment-analysis", model=name, truncation=True)


def score(text: str) -> dict:
    out = _model()(text[:512])[0]
    return {"label": out["label"].lower(), "score": float(out["score"]),
            "polarity": LABELS.get(out["label"].lower(), 0) * float(out["score"])}
