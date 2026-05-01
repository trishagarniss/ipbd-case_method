from __future__ import annotations
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from loguru import logger
from config.settings import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def upsert_markets(df: pd.DataFrame):
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