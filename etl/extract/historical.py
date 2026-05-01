from __future__ import annotations
import requests
import time
from loguru import logger
from config.settings import COINGECKO_BASE

TOP_COINS = [
    "bitcoin", "ethereum", "tether", "binancecoin", "solana",
    "ripple", "usd-coin", "staked-ether", "cardano", "avalanche-2",
    "dogecoin", "tron", "chainlink", "polkadot", "matic-network",
    "wrapped-bitcoin", "shiba-inu", "dai", "litecoin", "uniswap",
    "bitcoin-cash", "stellar", "monero", "ethereum-classic", "okb",
    "cosmos", "hedera-hashgraph", "filecoin", "internet-computer", "aptos",
    "quant-network", "vechain", "arbitrum", "near", "algorand",
    "the-graph", "fantom", "flow", "aave", "maker",
    "tezos", "theta-token", "axie-infinity", "decentraland", "sandbox",
    "gala", "chiliz", "enjincoin", "basic-attention-token", "curve-dao-token",
    "compound-governance-token", "yearn-finance", "sushi", "1inch",
    "loopring", "zcash", "dash", "neo", "waves", "iota"
]

def fetch_historical_bulk(coin_ids: list[str] = TOP_COINS) -> dict:
    """Tarik historical harga 60 koin dari CoinGecko (90 hari) = 5400 rows."""
    results = {}
    total = len(coin_ids)
    for i, coin_id in enumerate(coin_ids, 1):
        try:
            url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
            params = {"vs_currency": "usd", "days": 90, "interval": "daily"}
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            results[coin_id] = resp.json()
            logger.info(f"[Historical] {i}/{total} {coin_id} fetched")
            time.sleep(2)  # hindari rate limit CoinGecko 30 req/menit
        except Exception as e:
            logger.warning(f"[Historical] skip {coin_id}: {e}")
    logger.info(f"[Historical] selesai: {len(results)} coins")
    return results