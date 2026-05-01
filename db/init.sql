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
    UNIQUE (id, last_updated)
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
    UNIQUE (coin_id, date)
);
CREATE INDEX IF NOT EXISTS idx_historical_coin_date ON coins_historical (coin_id, date DESC);


-- Tabel 3: Fear & Greed Index dari alternative.me/fng
-- Indeks sentimen pasar crypto 0-100
-- 0-24: Extreme Fear, 25-49: Fear, 50-74: Greed, 75-100: Extreme Greed
-- Update: harian via Airflow DAG
CREATE TABLE IF NOT EXISTS fear_greed_daily (
    pk_id   BIGSERIAL   PRIMARY KEY,
    date    DATE        NOT NULL UNIQUE,
    value   INTEGER     NOT NULL,
    label   VARCHAR(50)
);

-- CREATE TABLE IF NOT EXISTS coincap_assets (
--     pk_id BIGSERIAL PRIMARY KEY,
--     id VARCHAR(100)    NOT NULL,
--     symbol VARCHAR(20),
--     name VARCHAR(100),
--     price_usd NUMERIC,
--     market_cap_usd NUMERIC,
--     volume_usd_24hr NUMERIC,
--     change_percent_24hr NUMERIC,
--     rank INTEGER,
--     -- DEFAULT NOW() dihapus — nilai WAJIB dikirim dari Python
--     -- pakai context["logical_date"] dari Airflow agar retry aman
--     fetched_at TIMESTAMPTZ NOT NULL,
--     UNIQUE (id, fetched_at)
-- );
-- CREATE INDEX IF NOT EXISTS idx_coincap_id ON coincap_assets (id);
-- CREATE INDEX IF NOT EXISTS idx_coincap_fetched_at ON coincap_assets (fetched_at DESC);