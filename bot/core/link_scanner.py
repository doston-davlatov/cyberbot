import re
import tldextract

phishing_keywords = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "confirm",
    "password",
    "wallet"
]

shorteners = [
    "bit.ly",
    "t.co",
    "tinyurl.com",
    "goo.gl",
    "ow.ly",
    "is.gd"
]


def extract_links(text):

    url_regex = r'(https?://[^\s]+)'
    return re.findall(url_regex, text)


def check_domain(url):

    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"
    return domain


def scan(text):

    links = extract_links(text)

    if not links:
        return {"danger": False}

    for link in links:

        domain = check_domain(link)

        for short in shorteners:
            if short in domain:
                return {
                    "danger": True,
                    "reason": "shortened_link"
                }

        for word in phishing_keywords:
            if word in link.lower():
                return {
                    "danger": True,
                    "reason": "phishing_keyword"
                }

    return {"danger": False}