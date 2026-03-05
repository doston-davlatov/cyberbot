# bot/core/text_analyzer.py
from bot.core.ai_model import is_phishing
import logging

logger = logging.getLogger(__name__)

SCAM_WORDS = {
    "uz": ["bank", "parol", "tasdiqlash", "yangilash"],
    "ru": ["банк", "пароль", "подтвердить", "обновить"],
    "en": ["bank", "password", "verify", "update"]
}

def analyze_text(text: str, lang: str = "en") -> dict:
    try:
        scam_words = SCAM_WORDS.get(lang, SCAM_WORDS["en"])
        if any(word in text.lower() for word in scam_words):
            return {"danger": True, "reason": "Scam so'zlar aniqlandi", "score": 1.0}

        is_danger, score = is_phishing(text)
        if is_danger:
            return {"danger": True, "reason": f"AI phishing: {score:.2%}", "score": score}

        return {"danger": False, "reason": "safe"}
    except Exception as e:
        logger.error(f"Matn analizda xato: {e}")
        return {"danger": False, "reason": "error"}