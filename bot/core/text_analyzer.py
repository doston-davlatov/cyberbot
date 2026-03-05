from .ai_model import analyze_text
from bot.utils import helpers

scam_words = [
    "send code",
    "verify account",
    "free money",
    "win prize",
    "urgent",
    "confirm password",
    "bank verification",
    "telegram support",
    "security alert",
    "click here"
]

def analyze(text, lang="en"):

    lower = text.lower()

    for word in scam_words:
        if word in lower:
            return {
                "danger": True,
                "reason": word
            }
    ai_result = analyze_text(text, lang)
    if ai_result["danger"]:
        return ai_result

    return {"danger": False}