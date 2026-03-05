from bot.database.mysql import execute, fetchone

def get_user(telegram_id):
    query = "SELECT * FROM users WHERE telegram_id = %s"
    return fetchone(query, (telegram_id,))


def create_user(telegram_id, username, language):
    query = """
    INSERT INTO users (telegram_id, username, language)
    VALUES (%s, %s, %s)
    """
    execute(query, (telegram_id, username, language))


def save_alert(group_id, user_id, message, threat_type, risk_level):
    query = """
    INSERT INTO alerts (group_id, user_id, message, threat_type, risk_level)
    VALUES (%s, %s, %s, %s, %s)
    """
    execute(query, (group_id, user_id, message, threat_type, risk_level))