# bot/handlers/files.py
from aiogram import Bot, Router, types
from aiogram import F
from aiogram.enums import ContentType
from bot.core.file_scanner import scan_file
from bot.database.models import get_user, save_alert
from bot.core.text_analyzer import analyze_text
from bot.core.link_scanner import extract_links, scan_link
from bot.utils.helpers import get_lang_text, notify_admins, get_user_language
from bot.utils.helpers import get_lang_text, notify_admins, get_user_language
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(F.document) 
async def handle_file(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    document = message.document
    file_info = await bot.get_file(document.file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    
    result = scan_file(file_url)
    
    if result["danger"]:
        user = get_user(user_id)
        save_alert(user["id"], "file", file_url, "high")
        await notify_admins(bot, f"Xavfli fayl: {file_url} (user: {user_id})")
        text = get_lang_text("malicious_file_alert", lang).format(reason=result["reason"])
    else:
        text = get_lang_text("file_safe", lang)
    
    await message.reply(text)