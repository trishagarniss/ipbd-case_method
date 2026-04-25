import pandas as pd
from sqlalchemy import create_engine
from loguru import logger
from config.settings import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def upsert_markets(df: pd.DataFrame):
    """Load data markets ke tabel coins_prices."""
    engine = get_engine()
    df.to_sql("coins_prices", engine, if_exists="append", index=False)
    logger.info(f"[Postgres] coins_prices: {len(df)} rows inserted")


def upsert_historical(df: pd.DataFrame):
    """Load historical data ke tabel coins_historical."""
    engine = get_engine()
    df.to_sql("coins_historical", engine, if_exists="append", index=False)
    logger.info(f"[Postgres] coins_historical: {len(df)} rows inserted")


def upsert_fear_greed(df: pd.DataFrame):
    """Load Fear & Greed ke tabel fear_greed_daily."""
    engine = get_engine()
    df.to_sql("fear_greed_daily", engine, if_exists="append", index=False)
    logger.info(f"[Postgres] fear_greed_daily: {len(df)} rows inserted")


def upsert_coincap(df: pd.DataFrame):
    """Load CoinCap data ke tabel coincap_assets."""
    engine = get_engine()
    df.to_sql("coincap_assets", engine, if_exists="append", index=False)
    logger.info(f"[Postgres] coincap_assets: {len(df)} rows inserted")
