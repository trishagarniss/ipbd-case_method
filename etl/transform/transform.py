import pandas as pd
from loguru import logger


def transform_markets(raw: list[dict]) -> pd.DataFrame:
    """Bersihkan & normalisasi data markets dari CoinGecko."""
    df = pd.DataFrame(raw)
    df = df[[
        "id", "symbol", "name", "current_price", "market_cap",
        "total_volume", "price_change_percentage_24h",
        "price_change_percentage_7d_in_currency",
        "circulating_supply", "last_updated"
    ]].copy()
    df.rename(columns={
        "price_change_percentage_7d_in_currency": "price_change_7d"
    }, inplace=True)
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df.dropna(subset=["current_price", "market_cap"], inplace=True)
    df["fetched_at"] = pd.Timestamp.utcnow()
    logger.info(f"[Transform] markets: {len(df)} rows cleaned")
    return df


def transform_historical(raw: dict, coin_id: str) -> pd.DataFrame:
    """Flatten historical market_chart ke tabular + hitung moving avg."""
    prices = raw.get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp_ms", "price"])
    df["coin_id"] = coin_id
    df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms").dt.date
    df["price_ma7"] = df["price"].rolling(7).mean()
    df["price_ma30"] = df["price"].rolling(30).mean()
    df["volatility"] = df["price"].pct_change().rolling(7).std()
    df.drop(columns=["timestamp_ms"], inplace=True)
    df.dropna(inplace=True)
    logger.info(f"[Transform] historical {coin_id}: {len(df)} rows")
    return df


def transform_fear_greed(raw: list[dict]) -> pd.DataFrame:
    """Normalisasi Fear & Greed data."""
    df = pd.DataFrame(raw)
    df = df[["value", "value_classification", "timestamp"]].copy()
    df["value"] = pd.to_numeric(df["value"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="s").dt.date
    df.drop(columns=["timestamp"], inplace=True)
    df.rename(columns={"value_classification": "label"}, inplace=True)
    logger.info(f"[Transform] fear_greed: {len(df)} rows cleaned")
    return df


def transform_coincap(raw: list[dict]) -> pd.DataFrame:
    """Normalisasi data dari CoinCap."""
    df = pd.DataFrame(raw)
    cols = ["id", "symbol", "name", "priceUsd", "marketCapUsd",
            "volumeUsd24Hr", "changePercent24Hr", "rank"]
    df = df[cols].copy()
    for col in ["priceUsd", "marketCapUsd", "volumeUsd24Hr", "changePercent24Hr"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce").astype("Int64")
    df["fetched_at"] = pd.Timestamp.utcnow()
    logger.info(f"[Transform] coincap: {len(df)} rows cleaned")
    return df
