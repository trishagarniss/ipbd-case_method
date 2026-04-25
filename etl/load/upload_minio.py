import boto3
import json
from datetime import datetime
from loguru import logger
from config.settings import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET


def get_client():
    return boto3.client(
        "s3",
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )


def ensure_bucket(client):
    existing = [b["Name"] for b in client.list_buckets().get("Buckets", [])]
    if MINIO_BUCKET not in existing:
        client.create_bucket(Bucket=MINIO_BUCKET)
        logger.info(f"[MinIO] bucket '{MINIO_BUCKET}' created")


def upload_raw(data: dict | list, source: str) -> str:
    """Upload raw JSON ke MinIO dengan path: raw/YYYY-MM-DD/HH-MM/{source}.json"""
    client = get_client()
    ensure_bucket(client)
    now = datetime.utcnow()
    key = f"raw/{now.strftime('%Y-%m-%d')}/{now.strftime('%H-%M')}/{source}.json"
    body = json.dumps(data, ensure_ascii=False)
    client.put_object(Bucket=MINIO_BUCKET, Key=key, Body=body, ContentType="application/json")
    logger.info(f"[MinIO] uploaded: {key}")
    return key
