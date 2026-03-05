# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env da topilmadi!")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "cyberbot_db")

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
if not VIRUSTOTAL_API_KEY:
    raise ValueError("VIRUSTOTAL_API_KEY .env da topilmadi!")

ADMINS = [int(admin.strip()) for admin in os.getenv("ADMINS", "").split(",") if admin.strip()]

SUPPORTED_LANGUAGES = ["uz", "ru", "en"]
DEFAULT_LANGUAGE = "uz"

LOG_FILE = "bot/utils/logs/bot.log"