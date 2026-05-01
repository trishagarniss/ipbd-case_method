from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, "/opt/airflow")

default_args = {
    "owner": "crypto-pipeline",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="dag_extract",
    default_args=default_args,
    description="Extract data dari 3 sumber API ke MinIO",
    schedule_interval="*/15 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "extract"],
) as dag:

    def extract_coingecko():
        from etl.extract.coingecko import fetch_markets
        from etl.load.upload_minio import upload_raw
        data = fetch_markets()
        upload_raw(data, "coingecko_markets")

    def extract_coincap():
        import requests
        from etl.load.upload_minio import upload_raw
        url = "https://api.coingecko.com/api/v3/global"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        upload_raw(data, "coingecko_global")

    def extract_fear_greed():
        from etl.extract.fear_greed import fetch_fear_greed
        from etl.load.upload_minio import upload_raw
        data = fetch_fear_greed(limit=365)
        upload_raw(data, "fear_greed")

    t1 = PythonOperator(task_id="extract_coingecko",  python_callable=extract_coingecko)
    t2 = PythonOperator(task_id="extract_coincap",    python_callable=extract_coincap)
    t3 = PythonOperator(task_id="extract_fear_greed", python_callable=extract_fear_greed)

    [t1, t2, t3]