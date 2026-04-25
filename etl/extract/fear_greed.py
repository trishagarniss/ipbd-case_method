from __future__ import annotations  # fix: Python 3.8 compat
import requests
from loguru import logger
from config.settings import FEARGREED_BASE


def fetch_fear_greed(limit: int = 365) -> list[dict]:
    """Tarik historical Fear & Greed Index (max 365 hari)."""
    url = f"{FEARGREED_BASE}/?limit={limit}&format=json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    logger.info(f"[FearGreed] {len(data)} days fetched")
    return data
