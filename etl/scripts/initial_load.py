from loguru import logger

from etl.extract.historical import fetch_historical_bulk
from etl.transform.transform import transform_historical
from etl.load.load_postgres import upsert_historical, upsert_dim_coins
from etl.extract.coingecko import fetch_markets
from etl.transform.transform import transform_markets
from etl.load.load_postgres import upsert_markets

def run_initial_load():
    logger.info("🚀 Memulai Proses Initial Load (Backfilling Data)...")
    
    # 1. Load markets dulu (buat ngisi dim_coins & harga saat ini)
    logger.info("Tahap 1: Mengambil data Markets...")
    try:
        raw_markets = fetch_markets()
        df_markets = transform_markets(raw_markets)
        upsert_markets(df_markets)
        logger.success(">> Tahap 1 Selesai: Data Markets & dim_coins berhasil disimpan.")
    except Exception as e:
        logger.error(f"❌ Tahap 1 Gagal: {e}")
        return

    # 2. Baru load historical
    logger.info("Tahap 2: Mengambil data Historical (90 Hari)...")
    try:
        raw_hist = fetch_historical_bulk()
        for coin_id, data in raw_hist.items():
            df = transform_historical(data, coin_id)
            upsert_historical(df)
            logger.info(f"   -> Historical data untuk '{coin_id}' tersimpan.")
        logger.success(">> Tahap 2 Selesai: Seluruh data Historical berhasil disimpan.")
    except Exception as e:
        logger.error(f"❌ Tahap 2 Gagal: {e}")

    logger.info("Proses Initial Load Selesai! Database sudah siap digunakan.")

if __name__ == "__main__":
    run_initial_load()