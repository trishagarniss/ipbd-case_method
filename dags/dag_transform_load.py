from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timezone
import sys
sys.path.insert(0, "/opt/airflow")

default_args = {
    "owner": "crypto-pipeline",
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="dag_transform_load",
    default_args=default_args,
    description="Transform + Load ke PostgreSQL",
    schedule_interval="*/15 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "transform", "load"],
) as dag:

    def transform_load_markets():
        from etl.extract.coingecko import fetch_markets
        from etl.transform.transform import transform_markets
        from etl.load.load_postgres import upsert_markets
        raw = fetch_markets()
        df = transform_markets(raw)
        upsert_markets(df)

    def transform_load_historical():
        from etl.extract.historical import fetch_historical_bulk
        from etl.transform.transform import transform_historical
        from etl.load.load_postgres import upsert_historical
        raw = fetch_historical_bulk()
        for coin_id, data in raw.items():
            df = transform_historical(data, coin_id)
            upsert_historical(df)

    def transform_load_fear_greed():
        from etl.extract.fear_greed import fetch_fear_greed
        from etl.transform.transform import transform_fear_greed
        from etl.load.load_postgres import upsert_fear_greed
        raw = fetch_fear_greed(limit=365)
        df = transform_fear_greed(raw)
        upsert_fear_greed(df)

    t1 = PythonOperator(
        task_id="tl_markets",
        python_callable=transform_load_markets,
    )
    t2 = PythonOperator(
        task_id="tl_coincap",
        python_callable=transform_load_historical,
    )
    t3 = PythonOperator(
        task_id="tl_fear_greed",
        python_callable=transform_load_fear_greed,
    )

    # paralel
    [t1, t2, t3]
