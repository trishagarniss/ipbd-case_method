# 🪙 Crypto Market Data Pipeline

Pipeline ETL end-to-end untuk data pasar kripto secara otomatis.  
Dibangun dengan Python · Apache Airflow · MinIO · PostgreSQL · Docker

---

## 🚀 Cara Menjalankan (dari Nol)

### 1. Clone repo
```bash
git clone https://github.com/username/crypto-pipeline.git
cd crypto-pipeline
```

### 2. Setup environment
```bash
cp .env.example .env
# Edit .env sesuai kebutuhan (password dll)
```

### 3. Jalankan semua service
```bash
docker compose up -d
```

### 4. Akses UI
| Service | URL | Kredensial |
|---------|-----|------------|
| Airflow | http://localhost:8080 | admin / admin |
| MinIO | http://localhost:9001 | minioadmin / minioadmin |
| Metabase | http://localhost:3000 | setup pertama kali |
| PostgreSQL | localhost:5432 | lihat .env |

### 5. Initial bulk load (5000+ rows)
```bash
# Jalankan sekali untuk tarik historical 90 hari
docker compose exec airflow-webserver python etl/scripts/initial_load.py
```

---

## 📁 Struktur Folder

```
crypto-pipeline/
├── dags/                   # Airflow DAG definitions
│   ├── dag_extract.py      # DAG: extract dari 3 API ke MinIO
│   └── dag_transform_load.py # DAG: transform + load ke Postgres
├── etl/
│   ├── extract/            # Script HTTP ke setiap API
│   ├── transform/          # Pandas cleaning & kalkulasi
│   └── load/               # Upsert ke Postgres & upload MinIO
├── db/
│   └── init.sql            # Skema tabel PostgreSQL
├── config/
│   └── settings.py         # Konfigurasi dari .env
├── logs/                   # Airflow & pipeline logs
├── notebooks/              # Eksplorasi & analisis
├── docker-compose.yml
├── .env.example
└── pyproject.toml
```

---

## 📊 Tabel Database

| Tabel | Isi | Update |
|-------|-----|--------|
| `coins_prices` | Snapshot harga 250 koin | Setiap 15 menit |
| `coins_historical` | Historical harga + MA7/MA30/volatility | Setiap hari |
| `coincap_assets` | Data aset dari CoinCap | Setiap 15 menit |
| `fear_greed_daily` | Fear & Greed Index harian | Setiap hari |

---

## 🛠️ Tech Stack

- **Orchestration**: Apache Airflow 2.8
- **Storage (raw)**: MinIO (S3-compatible object storage)
- **Warehouse**: PostgreSQL 14
- **Transform**: Pandas, NumPy
- **Visualisasi**: Metabase
- **Infra**: Docker Compose
- **VPS**: DigitalOcean (Singapore)
