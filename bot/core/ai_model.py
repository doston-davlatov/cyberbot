from transformers import pipeline
from bot.utils import helpers
import json
import os

LANG_DIR = os.path.join(os.path.dirname(__file__), "../languages")

def load_language(lang):
    path = os.path.join(LANG_DIR, f"{lang}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# DistilBERT modeli matnni scam yoki phishing uchun klassifikatsiya qiladi
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_text(text, lang="en"):

    result = classifier(text)[0]
    label = result["label"]
    score = result["score"]

    if label == "NEGATIVE" and score > 0.85:
        lang_data = load_language(lang)
        return {
            "danger": True,
            "score": score,
            "alert_text": lang_data.get("suspicious_text_alert", "Suspicious message detected")
        }

    return {
        "danger": False
    }