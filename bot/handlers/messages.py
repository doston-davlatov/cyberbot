# bot/handlers/messages.py
from aiogram import Bot
from aiogram import Router, types
from bot.core.text_analyzer import analyze_text
from bot.core.link_scanner import extract_links, scan_link
from bot.database.models import get_user, save_alert
from bot.utils.helpers import get_lang_text, notify_admins, get_user_language
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message()
async def handle_message(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    text = message.text or message.caption or ""
    
    # Matn analiz
    text_result = analyze_text(text, lang)
    
    # Havolalar
    links = extract_links(text)
    link_results = [scan_link(link) for link in links]
    any_link_danger = any(r["danger"] for r in link_results)
    
    if text_result["danger"] or any_link_danger:
        user = get_user(user_id)
        threat_type = "text" if text_result["danger"] else "link"
        content = text if text_result["danger"] else links[0]
        save_alert(user["id"], threat_type, content, "high")
        await notify_admins(bot, f"Xavf: {content} (user: {user_id})")
        text = get_lang_text("phishing_detected", lang).format(reason=text_result.get("reason", "") or link_results[0]["reason"])
    else:
        return  # Hech qanday xavf yo'q, javob bermaymiz
    
    await message.reply(text)