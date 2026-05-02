import requests
from airflow.models import Variable

def send_telegram_alert(context):
    bot_token = Variable.get("telegram_bot_token")
    chat_id = Variable.get("telegram_chat_id")
    
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    log_url = task_instance.log_url

    pesan = f"🚨 *AIRFLOW ETL ALERT* 🚨\n\n" \
            f"❌ *DAG:* `{dag_id}`\n" \
            f"📉 *Task:* `{task_id}` GAGAL!\n" \
            f"🔗 *Cek Log:* {log_url}\n\n" \
            f"Tolong cek server!"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': pesan, 'parse_mode': 'Markdown'}
    
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

    pesan = f"✅ *AIRFLOW ETL SUCCESS* ✅\n\n" \
            f"🚀 *DAG:* `{dag_id}`\n" \
            f"⏰ *Waktu:* `{execution_date}`\n\n" \
            f"Semua data berhasil ditarik dan di-load ke PostgreSQL. Dashboard aman! 😎"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': pesan, 'parse_mode': 'Markdown'}
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim notif Telegram: {e}")