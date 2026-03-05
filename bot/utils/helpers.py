import re

def extract_links(text):
    url_regex = r"(https?://[^\s]+)"
    return re.findall(url_regex, text)


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def truncate(text, length=100):
    if len(text) <= length:
        return text
    return text[:length] + "..."

def get_user_language(user):
    from bot.database.models import get_user
    db_user = get_user(user.id)
    if db_user and db_user.get("language") in ["uz", "ru", "en"]:
        return db_user.get("language")
    return "en"