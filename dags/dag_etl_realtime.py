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
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": send_telegram_alert,
}

with DAG(
    dag_id="dag_etl_realtime",
    default_args=default_args,
    description="Tarik harga pasar Real-Time",
    schedule_interval="*/15 * * * *", 
    max_active_runs=1,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "realtime", "markets"],
    on_success_callback=send_telegram_success,
) as dag:

    def transform_load_markets():
        from etl.extract.coingecko import fetch_markets
        from etl.transform.transform import transform_markets
        from etl.load.load_postgres import upsert_markets
        raw = fetch_markets()
        df = transform_markets(raw)
        upsert_markets(df)

    t1 = PythonOperator(task_id="tl_markets_realtime", python_callable=transform_load_markets)