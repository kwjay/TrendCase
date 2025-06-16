import numpy as np
import pandas as pd

def sma_crossover(data: pd.DataFrame, fast: int=50, slow: int=200) -> pd.DataFrame:
    df = data.copy()
    df[f"sma{fast}"] = df["close"].rolling(fast).mean()
    df[f"sma{slow}"] = df["close"].rolling(slow).mean()
    df["baseline"] = np.where(
        df[f"sma{fast}"] > df[f"sma{slow}"],
        "UP",
        np.where(df[f"sma{slow}"].notna(), "DOWN", "NAN")
    )
    return df

def rsi_threshold(data: pd.DataFrame, period: int=14, lower_bound: float=30, upper_bound: float=70) -> pd.DataFrame:
    df = data.copy()
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    roll_up = gain.ewm(span=period, adjust=False).mean()
    roll_down = loss.ewm(span=period, adjust=False).mean()
    rs = roll_up / roll_down
    df[f"RSI{period}"] = 100 - (100 / (1 + rs))
    df["baseline"] = np.where(
        df[f"RSI{period}"].notna() & (df[f"RSI{period}"] < lower_bound),
        "UP",
        np.where(df[f"RSI{period}"].notna() & (df[f"RSI{period}"] > upper_bound), "DOWN", "NAN")
    )
    return df