from __future__ import annotations  # fix: Python 3.8 compat
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from loguru import logger
from config.settings import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def upsert_markets(df: pd.DataFrame):
    """
    Upsert coins_prices.
    UNIQUE key: (id, last_updated) — pakai last_updated dari CoinGecko,
    bukan fetched_at, agar retry-safe meski waktu insert berbeda.
    """
    engine = get_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO coins_prices (
                    id, symbol, name, current_price, market_cap,
                    total_volume, price_change_percentage_24h, price_change_7d,
                    circulating_supply, last_updated, fetched_at
                ) VALUES (
                    :id, :symbol, :name, :current_price, :market_cap,
                    :total_volume, :price_change_percentage_24h, :price_change_7d,
                    :circulating_supply, :last_updated, :fetched_at
                )
                ON CONFLICT (id, last_updated) DO NOTHING
            """), row.to_dict())
    logger.info(f"[Postgres] coins_prices: {len(df)} rows upserted")


def upsert_historical(df: pd.DataFrame):
    """
    Upsert coins_historical.
    UNIQUE key: (coin_id, date) — 1 koin = 1 baris per hari.
    Kalau data hari yang sama sudah ada, skip.
    """
    engine = get_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO coins_historical (
                    coin_id, date, price, price_ma7, price_ma30, volatility
                ) VALUES (
                    :coin_id, :date, :price, :price_ma7, :price_ma30, :volatility
                )
                ON CONFLICT (coin_id, date) DO NOTHING
            """), row.to_dict())
    logger.info(f"[Postgres] coins_historical: {len(df)} rows upserted")


def upsert_fear_greed(df: pd.DataFrame):
    """
    Upsert fear_greed_daily.
    UNIQUE key: (date) — 1 baris per hari.
    Kalau ada data baru untuk hari yang sama, UPDATE nilainya.
    """
    engine = get_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO fear_greed_daily (date, value, label)
                VALUES (:date, :value, :label)
                ON CONFLICT (date) DO UPDATE
                    SET value = EXCLUDED.value,
                        label = EXCLUDED.label
            """), row.to_dict())
    logger.info(f"[Postgres] fear_greed_daily: {len(df)} rows upserted")


def upsert_coincap(df: pd.DataFrame, fetched_at: datetime):
    """
    Upsert coincap_assets.
    UNIQUE key: (id, fetched_at).
    fetched_at WAJIB dikirim dari DAG (pakai logical_date Airflow),
    bukan dari DEFAULT NOW() Postgres — agar retry menghasilkan key yang sama.
    """
    df = df.copy()
    df["fetched_at"] = fetched_at  # inject dari luar, bukan dari transform

    engine = get_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO coincap_assets (
                    id, symbol, name, price_usd, market_cap_usd,
                    volume_usd_24hr, change_percent_24hr, rank, fetched_at
                ) VALUES (
                    :id, :symbol, :name, :price_usd, :market_cap_usd,
                    :volume_usd_24hr, :change_percent_24hr, :rank, :fetched_at
                )
                ON CONFLICT (id, fetched_at) DO NOTHING
            """), row.to_dict())
    logger.info(f"[Postgres] coincap_assets: {len(df)} rows upserted")
