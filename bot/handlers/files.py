from aiogram import Router
from aiogram.types import Message
from bot.core import file_scanner
from bot.database import models
from bot.utils import helpers
import os
import json

router = Router()

LANG_DIR = os.path.join(os.path.dirname(__file__), "../languages")

def load_language(lang):
    path = os.path.join(LANG_DIR, f"{lang}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.message(content_types=["document"])
async def scan_file(message: Message):
    lang = helpers.get_user_language(message.from_user)
    lang_data = load_language(lang)

    file = await message.bot.get_file(message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}"

    result = file_scanner.scan(file_url)

    if result["danger"]:
        extra_text = f"File URL: {file_url}\n"
        if "malicious" in result:
            extra_text += f"Malicious: {result['malicious']}, Suspicious: {result['suspicious']}"
        await helpers.notify_admins(message, "malware_file_alert", "HIGH", lang_data, extra_text)
        models.save_alert(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            content=file_url,
            alert_type="malware_file",
            risk="high"
        )
        await message.reply(lang_data.get("malware_file_alert", "Fayl xavfli deb topildi!"))

def register(dp):
    dp.include_router(router)