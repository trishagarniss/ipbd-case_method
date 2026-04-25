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
        # import di dalam fungsi agar Airflow tidak parse saat load DAG
        from etl.extract.coingecko import fetch_markets
        from etl.load.upload_minio import upload_raw
        data = fetch_markets()
        upload_raw(data, "coingecko_markets")

    def extract_coincap():
        from etl.extract.coincap import fetch_assets
        from etl.load.upload_minio import upload_raw
        data = fetch_assets()
        upload_raw(data, "coincap_assets")

    def extract_fear_greed():
        from etl.extract.fear_greed import fetch_fear_greed
        from etl.load.upload_minio import upload_raw
        # limit=365 untuk initial load, ubah ke 1 setelah hari pertama
        data = fetch_fear_greed(limit=365)
        upload_raw(data, "fear_greed")

    t1 = PythonOperator(task_id="extract_coingecko",  python_callable=extract_coingecko)
    t2 = PythonOperator(task_id="extract_coincap",    python_callable=extract_coincap)
    t3 = PythonOperator(task_id="extract_fear_greed", python_callable=extract_fear_greed)

    # t1, t2, t3 jalan paralel — tidak ada dependency antar task
    [t1, t2, t3]
