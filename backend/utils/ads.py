from datetime import datetime
from pathlib import Path
import json
import requests

ads_cache = None
ads_cache_time = None
LOCAL_ADS_PATH = Path("/app/media/ads.json")
REMOTE_ADS_URL = "https://raw.githubusercontent.com/LiamAghamohammadi/whale-panel/main/media/ads.json"


def get_ads_from_github() -> dict:
    global ads_cache, ads_cache_time

    if (
        ads_cache
        and ads_cache_time
        and (datetime.now().timestamp() - ads_cache_time) < 3600
    ):
        return ads_cache

    try:
        if LOCAL_ADS_PATH.exists():
            with LOCAL_ADS_PATH.open("r", encoding="utf-8") as f:
                ads_data = json.load(f)
        else:
            response = requests.get(REMOTE_ADS_URL, timeout=5)
            response.raise_for_status()
            ads_data = response.json()

        ads_cache = ads_data
        ads_cache_time = datetime.now().timestamp()
        return ads_cache

    except (OSError, ValueError, requests.RequestException):
        default_ads = {
            "title": "نیاز به راهنمایی دارید؟",
            "text": "در صورت بروز مشکل یا داشتن سوال، تیم پشتیبانی در کنار شماست.",
            "link": "#",
            "button": "ارتباط با پشتیبانی",
        }
        ads_cache = default_ads
        ads_cache_time = datetime.now().timestamp()
        return default_ads
