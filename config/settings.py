import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.getenv("POSTGRES_DB", "crypto_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "crypto_user")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD", "yourpassword")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# MinIO
MINIO_ENDPOINT   = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET     = os.getenv("MINIO_BUCKET", "raw-crypto")

# API endpoints
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
COINCAP_BASE   = "https://api.coincap.io/v2"
FEARGREED_BASE = "https://api.alternative.me/fng"

# Pipeline config
COINS_PER_PAGE = 250
HISTORY_DAYS   = 90
