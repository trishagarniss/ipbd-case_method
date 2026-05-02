from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, "/opt/airflow")

from etl.utils.telegram_alerts import send_telegram_alert, send_telegram_success

default_args = {
    "owner": "crypto-pipeline",
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
    "on_failure_callback": send_telegram_alert,
}

with DAG(
    dag_id="dag_etl_daily",
    default_args=default_args,
    description="Tarik data Historical & Fear Greed (1x Sehari)",
    schedule_interval="0 2 * * *", 
    max_active_runs=1,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "daily", "historical", "fear_greed"],
    on_success_callback=send_telegram_success,
) as dag:

    def transform_load_historical():
        
        # Testing error handling & Telegram Alert
        # raise Exception("BOOM! Sengaja dibikin error buat ngetes Bot Telegram!")
        
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

    t1 = PythonOperator(task_id="tl_historical_daily", python_callable=transform_load_historical)
    t2 = PythonOperator(task_id="tl_fear_greed_daily", python_callable=transform_load_fear_greed)

    [t1, t2]