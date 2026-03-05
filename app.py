import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from bot.handlers import messages, commands, files
import config
from bot.utils import logger

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

messages.register(dp)
commands.register(dp)
files.register(dp)

logger.info("CyberGuard Bot ishga tushdi (Python 3.14, aiogram 3.x)")

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot ishga tushishda xato: {e}")

if __name__ == "__main__":
    asyncio.run(main())