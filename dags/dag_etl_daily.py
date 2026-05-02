from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import requests

sys.path.insert(0, "/opt/airflow")

def send_telegram_alert(context):
    bot_token = '8787792031:AAGWmM46bltDvCE8SoF33Kgcc2kaUChiPWU'
    chat_id = '-5113746384'
    
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    log_url = task_instance.log_url

    pesan = f"🚨 *AIRFLOW ETL ALERT* 🚨\n\n" \
            f"❌ *DAG:* `{dag_id}`\n" \
            f"📉 *Task:* `{task_id}` GAGAL!\n" \
            f"🔗 *Cek Log:* [Buka Airflow]({log_url})\n\n" \
            f"Tolong cek server!"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': pesan,
        'parse_mode': 'Markdown'
    }
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim notif Telegram: {e}")

def send_telegram_success(context):
    bot_token = '8787792031:AAGWmM46bltDvCE8SoF33Kgcc2kaUChiPWU'
    chat_id = '-5113746384'
    
    dag_run = context.get('dag_run')
    dag_id = dag_run.dag_id
    execution_date = context.get('execution_date').strftime("%Y-%m-%d %H:%M:%S")

    pesan = f"✅ *AIRFLOW ETL SUCCESS* ✅\n\n" \
            f"🚀 *DAG:* `{dag_id}`\n" \
            f"⏰ *Waktu:* `{execution_date}`\n\n" \
            f"Semua data berhasil ditarik dan di-load ke PostgreSQL. Dashboard aman! 😎"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': pesan,
        'parse_mode': 'Markdown'
    }
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim notif Telegram: {e}")

default_args = {
    "owner": "crypto-pipeline",
    "retries": 0,
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
        raise Exception("BOOM! Sengaja dibikin error buat ngetes Bot Telegram!")
        
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