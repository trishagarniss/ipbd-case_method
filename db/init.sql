-- Tabel 0: Dimensi Koin (Buku Induk Koin)
-- Dibuat pertama agar bisa direferensikan tabel lain
CREATE TABLE IF NOT EXISTS dim_coins (
    coin_id VARCHAR(100) PRIMARY KEY,
    symbol VARCHAR(20),
    name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabel 1: Snapshot harga real-time dari CoinGecko /coins/markets
-- Update: setiap 15 menit via Airflow DAG
CREATE TABLE IF NOT EXISTS coins_prices (
    pk_id BIGSERIAL PRIMARY KEY,
    id VARCHAR(100) NOT NULL,
    symbol VARCHAR(20),
    name VARCHAR(100),
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC,
    price_change_percentage_24h NUMERIC,
    price_change_7d NUMERIC,
    circulating_supply NUMERIC,
    last_updated TIMESTAMPTZ NOT NULL,
    fetched_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (id, last_updated),

    -- Relasi Foreign Key ke dim_coins
    CONSTRAINT fk_coin_prices FOREIGN KEY (id) REFERENCES dim_coins(coin_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_coins_prices_id ON coins_prices (id);
CREATE INDEX IF NOT EXISTS idx_coins_prices_last_updated ON coins_prices (last_updated DESC);


-- Tabel 2: Historical harga harian dari CoinGecko /coins/{id}/market_chart
-- Kalkulasi: moving average 7 hari, 30 hari, volatility
-- Update: harian via Airflow DAG
CREATE TABLE IF NOT EXISTS coins_historical (
    pk_id BIGSERIAL PRIMARY KEY,
    coin_id VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    price NUMERIC,
    price_ma7 NUMERIC,
    price_ma30 NUMERIC,
    volatility NUMERIC,
    UNIQUE (coin_id, date),

    -- Relasi Foreign Key ke dim_coins
    CONSTRAINT fk_coin_historical FOREIGN KEY (coin_id) REFERENCES dim_coins(coin_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_historical_coin_date ON coins_historical (coin_id, date DESC);


-- Tabel 3: Fear & Greed Index dari alternative.me/fng
-- Indeks sentimen pasar crypto 0-100
-- 0-24: Extreme Fear, 25-49: Fear, 50-74: Greed, 75-100: Extreme Greed
-- Update: harian via Airflow DAG
CREATE TABLE IF NOT EXISTS fear_greed_daily (
    pk_id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    value INTEGER NOT NULL,
    label VARCHAR(50)
);

-- Tabel 4: ETL Logging 
-- Mencatat riwayat eksekusi dan error dari Airflow
CREATE TABLE IF NOT EXISTS etl_logs (
    log_id BIGSERIAL PRIMARY KEY,
    dag_id VARCHAR(100),
    task_id VARCHAR(100),
    execution_date TIMESTAMPTZ,
    status VARCHAR(20),
    rows_processed INT DEFAULT 0,
    error_msg TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);