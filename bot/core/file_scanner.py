# bot/core/file_scanner.py
import requests
import hashlib
import logging
from virustotal_python import Virustotal
from config import VIRUSTOTAL_API_KEY

logger = logging.getLogger(__name__)

def scan_file(file_url: str) -> dict:
    try:
        # Faylni yuklab olish
        response = requests.get(file_url)
        response.raise_for_status()
        file_content = response.content

        # Hash hisoblash
        sha256 = hashlib.sha256(file_content).hexdigest()

        # VirusTotal orqali skan
        vtotal = Virustotal(API_KEY=VIRUSTOTAL_API_KEY)
        analysis = vtotal.request(f"files/{sha256}").json()

        if "data" in analysis:
            stats = analysis["data"]["attributes"]["last_analysis_stats"]
            malicious = stats.get("malicious", 0)
            if malicious > 0:
                return {"danger": True, "reason": f"{malicious} antivirus zararli deb topdi", "score": malicious}
        
        return {"danger": False, "reason": "safe"}
    except Exception as e:
        logger.error(f"Fayl skanida xato: {e}")
        return {"danger": False, "reason": "error"}