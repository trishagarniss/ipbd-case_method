from __future__ import annotations  # fix: Python 3.8 compat
import requests
import time
from loguru import logger
from config.settings import COINGECKO_BASE, COINS_PER_PAGE, HISTORY_DAYS


def fetch_markets() -> list[dict]:
    url = f"{COINGECKO_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": COINS_PER_PAGE,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d",
    }
    
    retries = 3
    while retries > 0:
        logger.info("[CoinGecko] Menarik data markets...")
        resp = requests.get(url, params=params, timeout=30)
        
        if resp.status_code == 429:
            logger.warning("⚠️ Kena Limit di markets! Istirahat 60 detik biar aman...")
            time.sleep(60)
            retries -= 1
            continue
            
        resp.raise_for_status()
        
        data = resp.json()
        logger.info(f"[CoinGecko] markets: {len(data)} coins fetched")
        return data
        
    # Kalau 3 kali ngulang kena limit terus
    raise Exception("Gagal menarik data markets setelah 3x percobaan.")


def fetch_historical(coin_id: str) -> dict:
    url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": HISTORY_DAYS, "interval": "daily"}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    logger.info(f"[CoinGecko] historical: {coin_id} fetched")
    return resp.json()


def bulk_historical(coin_ids: list[str]) -> dict:
    results = {}
    for coin_id in coin_ids:
        try:
            results[coin_id] = fetch_historical(coin_id)
        except Exception as e:
            logger.warning(f"[CoinGecko] skip {coin_id}: {e}")
    return results