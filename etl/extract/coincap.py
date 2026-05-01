from __future__ import annotations
import requests
from loguru import logger

def fetch_assets(limit: int = 200) -> dict:
    """Tarik global crypto market data dari CoinGecko (pengganti CoinCap)."""
    url = "https://api.coingecko.com/api/v3/global"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"[CoinGecko Global] market data fetched")
    return data