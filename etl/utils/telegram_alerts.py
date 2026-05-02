import requests
from airflow.models import Variable

def send_telegram_alert(context):
    bot_token = Variable.get("telegram_bot_token")
    chat_id = Variable.get("telegram_chat_id")
    
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    
    exec_date = context.get('execution_date').strftime("%Y-%m-%d %H:%M:%S")
    
    exception = context.get('exception')
    error_msg = str(exception)[:200] + "..." if len(str(exception)) > 200 else str(exception)
    
    airflow_url = "http://localhost:8081/home"

    pesan = f"🚨 <b>CRITICAL ETL FAILURE</b> 🚨\n\n" \
            f"<b>DAG:</b> <code>{dag_id}</code>\n" \
            f"<b>Task:</b> <code>{task_id}</code>\n" \
            f"<b>Waktu:</b> {exec_date}\n\n" \
            f"<b>Detail Error:</b>\n<pre>{error_msg}</pre>\n\n" \
            f"<a href='{airflow_url}'>Buka Dashboard Airflow</a>\n\n" \
            f"<b>>> Tolong segera cek server!</b>"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': pesan, 'parse_mode': 'HTML'}
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim notif Telegram: {e}")

def send_telegram_success(context):
    bot_token = Variable.get("telegram_bot_token")
    chat_id = Variable.get("telegram_chat_id")
    
    dag_run = context.get('dag_run')
    dag_id = dag_run.dag_id
    execution_date = context.get('execution_date').strftime("%Y-%m-%d %H:%M:%S")

    pesan = f"✅ <b>AIRFLOW ETL SUCCESS</b> ✅\n\n" \
            f"<b>DAG:</b> <code>{dag_id}</code>\n" \
            f"<b>Waktu:</b> <code>{execution_date}</code>\n\n" \
            f"<b>Semua data berhasil ditarik dan di-load ke PostgreSQL. Dashboard aman!</b> 😎"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': pesan, 'parse_mode': 'HTML'}
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim notif Telegram: {e}")