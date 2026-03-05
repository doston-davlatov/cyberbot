# bot/utils/helpers.py
import json
import os
import re
import logging
from aiogram import Bot
from bot.database.models import fetch_one
from config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

# Tarjimalarni yuklash
TRANSLATIONS = {}
languages_dir = "bot/languages"

if not os.path.exists(languages_dir):
    logger.error(f"Tarjimalar papkasi topilmadi: {languages_dir}")
else:
    for lang in SUPPORTED_LANGUAGES:
        file_path = os.path.join(languages_dir, f"{lang}.json")
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    TRANSLATIONS[lang] = json.load(f)
                logger.info(f"Tarjima yuklandi: {lang}.json ({len(TRANSLATIONS[lang])} ta kalit)")
            except Exception as e:
                logger.error(f"{lang}.json yuklashda xato: {e}")
        else:
            logger.warning(f"{lang}.json fayli topilmadi")

# Agar hech qanday til yuklanmasa
if not TRANSLATIONS:
    logger.critical("Hech qanday tarjima fayli yuklanmadi! Bot ishlamaydi.")
    # Bu yerda raise qilish mumkin, lekin hozircha davom etamiz

def get_lang_text(key: str, lang: str = None) -> str:
    """
    Berilgan kalit bo'yicha tarjima qaytaradi.
    Agar til yoki kalit topilmasa, fallback ishlatadi.
    """
    if lang is None:
        lang = DEFAULT_LANGUAGE

    # Til mavjud emas bo'lsa, default tilga o'tkazamiz
    if lang not in TRANSLATIONS:
        logger.warning(f"Til topilmadi: {lang}, fallback -> {DEFAULT_LANGUAGE}")
        lang = DEFAULT_LANGUAGE

    # Hali ham topilmasa (masalan DEFAULT_LANGUAGE ham yo'q)
    if lang not in TRANSLATIONS:
        logger.error(f"Default til ham yuklanmagan: {DEFAULT_LANGUAGE}")
        return f"[Tarjima topilmadi: {key}]"

    text = TRANSLATIONS[lang].get(key)
    if text is None:
        # Fallback: ingliz tilida izlash
        if lang != "en" and "en" in TRANSLATIONS and key in TRANSLATIONS["en"]:
            text = TRANSLATIONS["en"][key]
        else:
            text = f"[{key} not found in {lang}]"
        logger.debug(f"Kalit topilmadi: {key} ({lang}) → fallback ishlatildi")

    return text  # Faqat string qaytaramiz, .format ni bu yerda chaqirmaymiz!


def get_user_language(user_id: int) -> str:
    """Foydalanuvchi tilini DB dan oladi, topilmasa default qaytaradi"""
    try:
        user = fetch_one("SELECT language FROM users WHERE telegram_id = %s", (user_id,))
        if user and user["language"] in SUPPORTED_LANGUAGES:
            return user["language"]
    except Exception as e:
        logger.error(f"User tili olishda xato: {e}")

    return DEFAULT_LANGUAGE


async def notify_admins(bot: Bot, message: str):
    """Adminlarga xabar yuborish (config.py da ADMINS listi bo'lishi kerak)"""
    from config import ADMINS
    for admin_id in ADMINS:
        try:
            await bot.send_message(
                admin_id,
                f"⚠️ ADMIN ALERT:\n{message}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Admin {admin_id} ga xabar yuborishda xato: {e}")


def extract_links(text: str) -> list:
    """Matndan barcha havolalarni chiqarib beradi"""
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.findall(text)


def clean_text(text: str) -> str:
    """Matnni tozalash (ixtiyoriy, agar kerak bo'lsa)"""
    return text.strip()


def truncate(text: str, max_length: int = 100) -> str:
    """Matnni qisqartirish"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text