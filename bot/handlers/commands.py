from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils import helpers

router = Router()

@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    lang = helpers.get_user_language(message.from_user)
    await message.answer(helpers.get_lang_text("welcome_message", lang))

@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    lang = helpers.get_user_language(message.from_user)
    await message.answer(helpers.get_lang_text("help_message", lang))

def register(dp):
    dp.include_router(router)