# bot/handlers/commands.py
from aiogram import Router, types
from aiogram.filters import Command
from bot.utils.helpers import get_lang_text, get_user_language
from bot.database.models import create_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    create_user(user_id)
    lang = get_user_language(user_id)
    text = get_lang_text("welcome_message", lang)
    await message.answer(text)
    
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    text = get_lang_text("help_message", lang)
    await message.answer(text)