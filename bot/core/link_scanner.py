# bot/core/link_scanner.py
import re
import requests
from tldextract import extract
import logging

logger = logging.getLogger(__name__)

PHISHING_KEYWORDS = ["login", "password", "bank", "verify", "update", "secure"]
SHORTENERS = ["bit.ly", "goo.gl", "tinyurl.com"]

def extract_links(text: str) -> list:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.findall(text)

def scan_link(url: str) -> dict:
    try:
        # Domen tekshirish
        extracted = extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"

        if domain in SHORTENERS:
            response = requests.head(url, allow_redirects=True)
            url = response.url  # Real URL olish

        # Keywords tekshirish
        if any(kw in url.lower() for kw in PHISHING_KEYWORDS):
            return {"danger": True, "reason": "Phishing keywords aniqlandi", "score": 1.0}

        # Qo'shimcha: VT yoki Safe Browsing qo'shish mumkin

        return {"danger": False, "reason": "safe"}
    except Exception as e:
        logger.error(f"Havola skanida xato: {e}")
        return {"danger": False, "reason": "error"}