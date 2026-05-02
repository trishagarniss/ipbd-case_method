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
    "loopring", "zcash", "dash", "neo", "waves", "iota",
    "toncoin", "optimism", "pepe", "injective-protocol", "kaspa",
    "cronos", "mantle", "render", "immutable-x", "thorchain",
    "celestia", "sui", "sei", "floki", "bonk",
    "arweave", "dydx", "blur", "jupiter", "pyth-network",
    "gmx", "synthetix-network-token", "pancakeswap-token", "lido-dao", "eos",
    "kava", "mina", "trust-wallet-token", "conflux-token", "woo-network",
    "zilliqa", "pax-gold", "kucoin-shares", "huobi-token", "bitget-token",
    "nexo", "pendle", "akash-network", "helium", "singularitynet"
]

def fetch_historical_bulk(coin_ids: list[str] = TOP_COINS) -> dict:
    """Tarik historical harga 60 koin dengan sistem Anti-Blokir (Retry)."""
    results = {}
    total = len(coin_ids)
    
    for i, coin_id in enumerate(coin_ids, 1):
        success = False
        retries = 3
        
        while not success and retries > 0:
            try:
                url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
                params = {"vs_currency": "usd", "days": 90, "interval": "daily"}
                
                logger.info(f"[Historical] Menarik data {i}/{total} {coin_id}...")
                resp = requests.get(url, params=params, timeout=30)
                
                # Cek apakah kita kena limit API CoinGecko (Error 429)
                if resp.status_code == 429:
                    logger.warning(f"⚠️ Kena Limit di {coin_id}! Istirahat 60 detik biar aman...")
                    time.sleep(60)
                    retries -= 1
                    continue # Langsung coba lagi koin yang sama tanpa skip
                
                resp.raise_for_status() # Cek error lain selain 429
                
                # Kalau eksekusi sukses sampai sini
                results[coin_id] = resp.json()
                logger.info(f"✅ Berhasil: {coin_id}")
                success = True
                time.sleep(15) # Jeda normal 15 detik biar sopan ke server
                
            except Exception as e:
                logger.error(f"❌ Error lain di {coin_id}: {e}")
                time.sleep(30)
                retries -= 1
                
        if not success:
            logger.error(f"🚨 Gagal total narik {coin_id} setelah 3x coba. Skip ke koin berikutnya.")

    logger.info(f"[Historical] Proses selesai. Berhasil ditarik: {len(results)}/{total} coins")
    return results