from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from app.config import MODEL_NAME

FALLBACK_MODEL = "ProsusAI/finbert"


import re
from newspaper import Article

def build_sentiment_pipeline():
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    except Exception as exc:  # pragma: no cover - defensive fallback for missing files
        print(f"Primary model '{MODEL_NAME}' failed to load, falling back to '{FALLBACK_MODEL}'. Error: {exc}")
        tokenizer = AutoTokenizer.from_pretrained(FALLBACK_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(FALLBACK_MODEL)

    return pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        top_k=None,
    )


def normalize_label(label: str) -> str:
    text = label.strip().lower()
    mapping = {
        "pos": "positive",
        "positive": "positive",
        "neg": "negative",
        "negative": "negative",
        "neu": "neutral",
        "neutral": "neutral",
    }
    return mapping.get(text, text)


def decide_label(scores, uncertainty_threshold: float) -> str:
    """
    scores: list of {'label': str, 'score': float} sorted desc
    uncertainty_threshold in [0, 1], e.g. 0.4

    Returns: 'positive'/'neutral'/'negative' or 'uncertain'
    """
    if not scores:
        return "uncertain"

    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    top = scores[0]
    second = scores[1] if len(scores) > 1 else {"score": 0.0}

    if top["score"] < (1 - uncertainty_threshold):
        return "uncertain"
    if (top["score"] - second["score"]) < (uncertainty_threshold / 2):
        return "uncertain"

    return top["label"]


def predict_sentiment(pipeline_obj, text: str):
    outputs = pipeline_obj(text)
    
    # Handle list of lists (when top_k is used, modern huggingface pipelines return [[{label, score}, ...]])
    if isinstance(outputs, list) and len(outputs) > 0 and isinstance(outputs[0], list):
        raw_scores = outputs[0]
    else:
        raw_scores = outputs
        
    # If the pipeline inexplicably returns a single dict within the list for some models:
    if isinstance(raw_scores, dict): 
        raw_scores = [raw_scores]
        
    scores = [
        {"label": normalize_label(item["label"]), "score": float(item["score"])}
        for item in raw_scores
    ]
    scores = sorted(scores, key=lambda item: item["score"], reverse=True)
    top = scores[0]
    return top["label"], top["score"], scores

def extract_article_from_url(url: str):
    """Downloads and parses an article from a URL using newspaper3k."""
    article = Article(url)
    try:
        article.download()
        article.parse()
        return article.title, article.text, list(article.authors), article.publish_date
    except Exception as e:
        return None, f"Failed to extract article: {str(e)}", [], None

def split_into_sentences(text: str):
    """Simple regex-based sentence splitter for article analysis."""
    sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def analyze_article_sentences(pipeline_obj, sentences, threshold):
    results = []
    for sentence in sentences:
        try:
            label, score, all_scores = predict_sentiment(pipeline_obj, sentence[:512])
            final_label = label
            if score < threshold:
                final_label = "uncertain"
            results.append({
                "sentence": sentence,
                "label": final_label,
                "confidence": score,
                "all_scores": all_scores
            })
        except Exception:
            pass # Skip failing sentences
    return results

def summarize_article_results(results):
    if not results:
        return {"positive": 0, "neutral": 0, "negative": 0, "uncertain": 0, "total": 0}
        
    summary = {"positive": 0, "neutral": 0, "negative": 0, "uncertain": 0, "total": len(results)}
    for r in results:
        lbl = r["label"]
        if lbl in summary:
            summary[lbl] += 1
            
    return summary


