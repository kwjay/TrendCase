import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import pandas as pd

load_dotenv()
API_KEY: str | None = os.getenv("ALPHA_API_KEY")
API_URL = "https://www.alphavantage.co/query"

def fetch_daily(symbol: str, output_size:str="compact") -> pd.DataFrame:
    if API_KEY is None:
        raise RuntimeError("ALPHA_API_KEY is not set.")
    params = {"function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": output_size,
            "datatype": "json",
            "apikey": API_KEY}
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    df = (pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            .rename_axis("date")
            .rename(columns=lambda col: col.split(". ")[1])
            .astype(float)
            .sort_index())
    df["volume"] = df["volume"].astype(int)
    return df

def daily_path(symbol: str, root: str | os.PathLike="data") -> Path:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    return root / f"{symbol.upper()}_daily.parquet"

def load_daily(symbol: str, root: str | os.PathLike="data") -> pd.DataFrame | None:
    path = daily_path(symbol, root)
    if path.exists():
        return pd.read_parquet(path)
    return None

def save_daily(df: pd.DataFrame, symbol: str, root: str | os.PathLike="data") -> None:
    path = daily_path(symbol, root)
    df.to_parquet(path, engine="auto", index=True)

def get_daily(symbol: str, root: str | os.PathLike="data") -> pd.DataFrame:
    daily = load_daily(symbol, root)
    if daily is None:
        df = fetch_daily(symbol, "full")
        save_daily(df, symbol, root)
        return df

    oldest_entry = daily.index.max()
    new_data = fetch_daily(symbol, "compact")
    new_entries = new_data[new_data.index > oldest_entry]
    if new_entries.empty:
        return daily
    updated_daily = (
        pd.concat([daily, new_entries])
        .sort_index()
        .astype({"volume": "int64"})
    )
    save_daily(updated_daily, symbol, root)
    return updated_daily