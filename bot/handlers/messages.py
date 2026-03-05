from aiogram import Router
from aiogram.types import Message
from bot.core.text_analyzer import analyze
from bot.utils import helpers
from bot.database import models
from bot.core.link_scanner import scan_link

router = Router()

@router.message()
async def message_handler(message: Message):
    lang = helpers.get_user_language(message.from_user)
    
    # AI + scam matn tekshiruv
    result = analyze(message.text, lang)
    if result["danger"]:
        await message.reply(result.get("alert_text", "Xavfli xabar aniqlandi!"))
        # Adminga alert yuborish
        await helpers.notify_admins(message, "suspicious_text_alert", result.get("reason",""), lang)
        # DB ga saqlash
        models.save_alert(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            content=message.text,
            alert_type="text",
            risk="high"
        )
        return

    # Havolalarni tekshirish
    urls = scan_link.extract_urls(message.text)
    for url in urls:
        is_danger = scan_link.scan(url)
        if is_danger:
            await helpers.notify_admins(message, "malicious_link_alert", url, lang)
            await message.reply("Havola xavfli deb topildi!")
            models.save_alert(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                content=url,
                alert_type="link",
                risk="high"
            )

def register(dp):
    dp.include_router(router)