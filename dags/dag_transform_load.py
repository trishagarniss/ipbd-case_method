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

    def transform_load_coincap(**context):
        from etl.extract.coincap import fetch_assets
        from etl.transform.transform import transform_coincap
        from etl.load.load_postgres import upsert_coincap

        # pakai logical_date dari Airflow — TIDAK berubah saat retry
        # ini yang membuat UNIQUE (id, fetched_at) bisa menolak duplikat
        logical_date = context["logical_date"]
        if logical_date.tzinfo is None:
            logical_date = logical_date.replace(tzinfo=timezone.utc)

        raw = fetch_assets()
        df = transform_coincap(raw)
        upsert_coincap(df, fetched_at=logical_date)  # inject dari luar

    def transform_load_fear_greed():
        from etl.extract.fear_greed import fetch_fear_greed
        from etl.transform.transform import transform_fear_greed
        from etl.load.load_postgres import upsert_fear_greed
        raw = fetch_fear_greed(limit=1)
        df = transform_fear_greed(raw)
        upsert_fear_greed(df)

    t1 = PythonOperator(
        task_id="tl_markets",
        python_callable=transform_load_markets,
    )
    t2 = PythonOperator(
        task_id="tl_coincap",
        python_callable=transform_load_coincap,
        # provide_context deprecated di Airflow 2.x, pakai **context otomatis
    )
    t3 = PythonOperator(
        task_id="tl_fear_greed",
        python_callable=transform_load_fear_greed,
    )

    # paralel — semua task jalan bersamaan
    [t1, t2, t3]
