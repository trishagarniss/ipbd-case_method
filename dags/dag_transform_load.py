from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
import sys
sys.path.insert(0, "/opt/airflow")

from etl.extract.coingecko import fetch_markets
from etl.extract.coincap import fetch_assets
from etl.extract.fear_greed import fetch_fear_greed
from etl.transform.transform import (
    transform_markets, transform_coincap, transform_fear_greed
)
from etl.load.load_postgres import (
    upsert_markets, upsert_coincap, upsert_fear_greed
)

default_args = {
    "owner": "crypto-pipeline",
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="dag_transform_load",
    default_args=default_args,
    description="Transform data dari MinIO & load ke PostgreSQL",
    schedule_interval="*/15 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "transform", "load"],
) as dag:

    def transform_load_markets():
        raw = fetch_markets()
        df = transform_markets(raw)
        upsert_markets(df)

    def transform_load_coincap():
        raw = fetch_assets()
        df = transform_coincap(raw)
        upsert_coincap(df)

    def transform_load_fear_greed():
        raw = fetch_fear_greed(limit=1)
        df = transform_fear_greed(raw)
        upsert_fear_greed(df)

    t1 = PythonOperator(task_id="tl_markets",    python_callable=transform_load_markets)
    t2 = PythonOperator(task_id="tl_coincap",    python_callable=transform_load_coincap)
    t3 = PythonOperator(task_id="tl_fear_greed", python_callable=transform_load_fear_greed)

    [t1, t2, t3]
