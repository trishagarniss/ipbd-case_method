-- Tabel utama: snapshot harga dari CoinGecko
CREATE TABLE IF NOT EXISTS coins_prices (
    id                      VARCHAR(100),
    symbol                  VARCHAR(20),
    name                    VARCHAR(100),
    current_price           NUMERIC,
    market_cap              NUMERIC,
    total_volume            NUMERIC,
    price_change_percentage_24h NUMERIC,
    price_change_7d         NUMERIC,
    circulating_supply      NUMERIC,
    last_updated            TIMESTAMPTZ,
    fetched_at              TIMESTAMPTZ DEFAULT NOW()
);

-- Tabel historical: harga harian + moving avg
CREATE TABLE IF NOT EXISTS coins_historical (
    coin_id     VARCHAR(100),
    date        DATE,
    price       NUMERIC,
    price_ma7   NUMERIC,
    price_ma30  NUMERIC,
    volatility  NUMERIC
);

-- Tabel Fear & Greed Index
CREATE TABLE IF NOT EXISTS fear_greed_daily (
    date    DATE,
    value   INTEGER,
    label   VARCHAR(50)
);

-- Tabel CoinCap assets
CREATE TABLE IF NOT EXISTS coincap_assets (
    id                  VARCHAR(100),
    symbol              VARCHAR(20),
    name                VARCHAR(100),
    "priceUsd"          NUMERIC,
    "marketCapUsd"      NUMERIC,
    "volumeUsd24Hr"     NUMERIC,
    "changePercent24Hr" NUMERIC,
    rank                INTEGER,
    fetched_at          TIMESTAMPTZ DEFAULT NOW()
);
