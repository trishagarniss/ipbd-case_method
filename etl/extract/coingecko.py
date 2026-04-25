import requests
import json
from datetime import datetime
from loguru import logger
from config.settings import COINGECKO_BASE, COINS_PER_PAGE, HISTORY_DAYS


def fetch_markets() -> list[dict]:
    """Tarik snapshot harga 250 koin sekaligus."""
    url = f"{COINGECKO_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": COINS_PER_PAGE,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"[CoinGecko] markets: {len(data)} coins fetched")
    return data


def fetch_historical(coin_id: str) -> dict:
    """Tarik historical harga 1 koin (90 hari)."""
    url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": HISTORY_DAYS, "interval": "daily"}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    logger.info(f"[CoinGecko] historical: {coin_id} fetched")
    return resp.json()


def bulk_historical(coin_ids: list[str]) -> dict:
    """Tarik historical untuk list koin — untuk initial load 5000+ rows."""
    results = {}
    for coin_id in coin_ids:
        try:
            results[coin_id] = fetch_historical(coin_id)
        except Exception as e:
            logger.warning(f"[CoinGecko] skip {coin_id}: {e}")
    return results
