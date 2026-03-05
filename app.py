# app.py
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.core.ai_model import load_phishing_model
from bot.utils.logger import setup_logger
from bot.handlers import commands, messages, files
from config import BOT_TOKEN, LOG_FILE

async def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Bot ishga tushmoqda...")

    load_phishing_model()

    bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(messages.router)
    dp.include_router(files.router)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot ishga tushishda xato: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    asyncio.run(main())