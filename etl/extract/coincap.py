from __future__ import annotations  # fix: Python 3.8 compat
import requests
from loguru import logger
from config.settings import COINCAP_BASE


def fetch_assets(limit: int = 200) -> list[dict]:
    """Tarik 200 aset crypto dari CoinCap."""
    url = f"{COINCAP_BASE}/assets"
    params = {"limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    logger.info(f"[CoinCap] assets: {len(data)} coins fetched")
    return data
