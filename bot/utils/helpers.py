# bot/utils/helpers.py
import json
import os
import re
from aiogram import Bot
import logging
from bot.database.models import fetch_one
from config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

TRANSLATIONS = {}
def get_lang_text(key: str, lang: str = "uz") -> str:
    """
    Tarjima qaytaradi. Agar til yoki key topilmasa, ingliz yoki placeholder ishlatadi.
    """
    if lang not in TRANSLATIONS:
        lang = DEFAULT_LANGUAGE  
    if key not in TRANSLATIONS[lang]:
        if lang != DEFAULT_LANGUAGE and key in TRANSLATIONS.get(DEFAULT_LANGUAGE, {}):
            return TRANSLATIONS[DEFAULT_LANGUAGE][key]
        return f"[{key} not found in {lang}]"

    text = TRANSLATIONS[lang][key]
    return text 

def get_user_language(user_id: int) -> str:
    user = fetch_one("SELECT language FROM users WHERE telegram_id = %s", (user_id,))
    return user["language"] if user else DEFAULT_LANGUAGE

async def notify_admins(bot: Bot, message: str):
    from config import ADMINS
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, f"⚠️ ALERT: {message}")
        except Exception as e:
            logger.error(f"Admin notify xato: {e}")

def extract_links(text: str) -> list:
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.findall(text)