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
    dag_id="dag_extract_realtime",
    default_args=default_args,
    description="Extract data pasar Real-Time ke MinIO",
    schedule_interval=None,
    max_active_runs=1,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "extract", "realtime"],
    # on_success_callback=send_telegram_success,
) as dag:

    def extract_coingecko():
        from etl.extract.coingecko import fetch_markets
        from etl.load.upload_minio import upload_raw
        data = fetch_markets()
        upload_raw(data, "coingecko_markets")

    t1 = PythonOperator(task_id="extract_coingecko", python_callable=extract_coingecko)