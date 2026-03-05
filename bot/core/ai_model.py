# bot/core/ai_model.py
from transformers import pipeline
import torch
import logging

logger = logging.getLogger(__name__)

PHISHING_MODEL = None

def load_phishing_model():
    global PHISHING_MODEL
    try:
        PHISHING_MODEL = pipeline(
            "text-classification",
            model="cybersectony/phishing-email-detection-distilbert_v2.4.1",
            device=0 if torch.cuda.is_available() else -1
        )
        logger.info("Phishing model yuklandi")
    except Exception as e:
        logger.error(f"Model yuklashda xato: {e}")

def is_phishing(text: str, threshold: float = 0.75) -> tuple[bool, float]:
    if PHISHING_MODEL is None:
        load_phishing_model()
        if PHISHING_MODEL is None:
            return False, 0.0

    try:
        results = PHISHING_MODEL(text, truncation=True, max_length=512)
        for res in results:
            if res['label'].lower() in ['phishing', 'malicious']:
                score = res['score']
                if score >= threshold:
                    return True, score
        return False, 0.0
    except Exception as e:
        logger.error(f"AI analizda xato: {e}")
        return False, 0.0