# bot/database/models.py
from bot.database.mysql import execute_query, fetch_one
import logging

logger = logging.getLogger(__name__)

def get_user(telegram_id: int):
    query = "SELECT * FROM users WHERE telegram_id = %s"
    return fetch_one(query, (telegram_id,))

def create_user(telegram_id: int, language: str = "uz"):
    if get_user(telegram_id):
        return  
    query = "INSERT INTO users (telegram_id, language) VALUES (%s, %s)"
    execute_query(query, (telegram_id, language))

def save_alert(user_id: int, threat_type: str, content: str, risk_level: str = "medium"):
    query = "INSERT INTO alerts (user_id, threat_type, content, risk_level) VALUES (%s, %s, %s, %s)"
    execute_query(query, (user_id, threat_type, content, risk_level))