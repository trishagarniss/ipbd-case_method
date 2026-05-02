from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, "/opt/airflow")

from etl.utils.telegram_alerts import send_telegram_alert, send_telegram_success


default_args = {
    "owner": "crypto-pipeline",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": send_telegram_alert,
}

with DAG(
    dag_id="dag_extract_daily",
    default_args=default_args,
    description="Extract data Historical & Fear Greed ke MinIO (1x Sehari)",
    schedule_interval="0 1 * * *",
    max_active_runs=1,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "extract", "daily"],
    on_success_callback=send_telegram_success,
) as dag:

    def extract_historical():
        from etl.extract.historical import fetch_historical_bulk
        from etl.load.upload_minio import upload_raw
        data = fetch_historical_bulk()
        upload_raw(data, "coingecko_historical")

    def extract_fear_greed():
        from etl.extract.fear_greed import fetch_fear_greed
        from etl.load.upload_minio import upload_raw
        data = fetch_fear_greed(limit=365)
        upload_raw(data, "fear_greed")

    t1 = PythonOperator(task_id="extract_historical_daily", python_callable=extract_historical)
    t2 = PythonOperator(task_id="extract_fear_greed_daily", python_callable=extract_fear_greed)

    [t1, t2]