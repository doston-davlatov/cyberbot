import requests
import hashlib
import config

VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/files"


def download_file(url):

    response = requests.get(url)

    if response.status_code == 200:
        return response.content

    return None


def file_hash(data):

    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


def scan(file_url):

    data = download_file(file_url)

    if not data:
        return {"danger": False}

    hash_value = file_hash(data)

    headers = {
        "x-apikey": config.VIRUSTOTAL_API_KEY
    }

    response = requests.get(
        f"{VIRUSTOTAL_URL}/{hash_value}",
        headers=headers
    )

    if response.status_code != 200:
        return {"danger": False}

    result = response.json()

    stats = result["data"]["attributes"]["last_analysis_stats"]

    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)

    if malicious > 0 or suspicious > 0:
        return {
            "danger": True,
            "malicious": malicious,
            "suspicious": suspicious
        }

    return {"danger": False}