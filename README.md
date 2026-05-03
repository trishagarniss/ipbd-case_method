# 🪙 Crypto Market Data Pipeline

Pipeline ETL end-to-end untuk data pasar kripto secara otomatis dengan fitur logging dan monitoring.  
Dibangun dengan Python · Apache Airflow · MinIO · PostgreSQL · Docker · Azure

---

## Cara Menjalankan (Deployment)

### 1. Clone repo
```bash
git clone https://github.com/trishagarniss/ipbd-case_method.git
cd ipbd-case_method
```

### 2. Setup environment
```bash
# Buat file .env dan sesuaikan kredensial
nano .env 
```

### 3. Jalankan semua service
```bash
# Build image untuk menginstall dependencies (loguru, pandas, dll)
docker compose up -d --build
```

### 4. Initial Load (Manual Trigger)
Jalankan ini sekali untuk menarik data historical 90 hari dan mengisi tabel logs awal[cite: 4]:
```bash
docker exec -it ipbd-case_method-airflow-worker-1 python -m etl.scripts.initial_load
```

### 5. Akses UI
| Service | URL | Kredensial |
|---------|-----|------------|
| **Airflow** | http://20.41.104.165:8080 | admin / admin |
| **MinIO** | http://20.41.104.165:9001 | minio_admin / SecretKeyMinio! |
| **Metabase** | http://20.41.104.165:3000 | setup pertama kali |

---

## 📁 Struktur Folder

```
ipbd-case_method/
├── dags/                # Definisi Orchestration Airflow
├── etl/
│   ├── extract/         # Script penarikan API (CoinGecko, Fear&Greed)
│   ├── transform/       # Cleaning & kalkulasi (MA7, MA30, Volatility)
│   └── load/            # Upsert ke Postgres & logging mechanism[cite: 4]
├── db/
│   └── init.sql         # Skema tabel database (termasuk etl_logs)
├── config/
│   └── settings.py      # Konfigurasi environment variabel[cite: 2]
├── docker-compose.yml   # Orchestration container
└── requirements.txt     # Python dependencies
```

---

## 📊 Monitoring & Logging
Pipeline ini dilengkapi dengan tabel `etl_logs` yang mencatat setiap eksekusi task:
- **Status**: SUCCESS / FAILED.
- **Metrics**: Jumlah baris data yang berhasil diproses.
- **Error Tracking**: Pesan error otomatis tercatat jika task gagal[cite: 4].

---

## 🛠️ Tech Stack
- **Orchestration**: Apache Airflow
- **Storage (Raw)**: MinIO (S3-compatible)
- **Warehouse**: PostgreSQL
- **Transform**: Pandas & SQLAlchemy
- **Infrastructure**: Docker Compose
- **Cloud**: Microsoft Azure (Ubuntu 22.04 LTS)
```
