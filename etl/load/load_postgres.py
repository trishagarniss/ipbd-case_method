from __future__ import annotations
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from loguru import logger
from config.settings import DATABASE_URL

def get_engine():
    return create_engine(DATABASE_URL)

def log_etl_execution(dag_id: str, task_id: str, status: str, rows_processed: int = 0, error_msg: str = None):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO etl_logs (dag_id, task_id, execution_date, status, rows_processed, error_msg, created_at)
            VALUES (:dag_id, :task_id, NOW(), :status, :rows_processed, :error_msg, NOW())
        """), {
            "dag_id": dag_id,
            "task_id": task_id,
            "status": status,
            "rows_processed": rows_processed,
            "error_msg": error_msg
        })
    logger.info(f"[ETL Log] {task_id} logged as {status} ({rows_processed} rows)")

def upsert_dim_coins(df: pd.DataFrame, dag_id: str = "manual_load"):
    engine = get_engine()
    
    dim_df = df[['id', 'symbol', 'name']].drop_duplicates()
    
    try:
        with engine.begin() as conn:
            for _, row in dim_df.iterrows():
                conn.execute(text("""
                    INSERT INTO dim_coins (coin_id, symbol, name)
                    VALUES (:id, :symbol, :name)
                    ON CONFLICT (coin_id) DO NOTHING
                """), row.to_dict())
        logger.info(f"[Postgres] dim_coins: {len(dim_df)} rows upserted")
        # Log success
        log_etl_execution(dag_id, "upsert_dim_coins", "SUCCESS", len(dim_df))
    except Exception as e:
        log_etl_execution(dag_id, "upsert_dim_coins", "FAILED", 0, str(e))
        raise e

def upsert_markets(df: pd.DataFrame, dag_id: str = "manual_load"):
    upsert_dim_coins(df, dag_id)
    
    engine = get_engine()
    try:
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
        # Log success
        log_etl_execution(dag_id, "upsert_markets", "SUCCESS", len(df))
    except Exception as e:
        log_etl_execution(dag_id, "upsert_markets", "FAILED", 0, str(e))
        raise e

def upsert_historical(df: pd.DataFrame, dag_id: str = "manual_load"):
    engine = get_engine()
    
    try:
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
        # Log success
        log_etl_execution(dag_id, "upsert_historical", "SUCCESS", len(df))
    except Exception as e:
        log_etl_execution(dag_id, "upsert_historical", "FAILED", 0, str(e))
        raise e

def upsert_fear_greed(df: pd.DataFrame, dag_id: str = "manual_load"):
    engine = get_engine()
    
    try:
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
        # Log success
        log_etl_execution(dag_id, "upsert_fear_greed", "SUCCESS", len(df))
    except Exception as e:
        log_etl_execution(dag_id, "upsert_fear_greed", "FAILED", 0, str(e))
        raise e