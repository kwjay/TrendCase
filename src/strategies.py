import pandas as pd


def sma_crossover(data: pd.DataFrame) -> pd.DataFrame:
    data["SMA50"] = data["Close"].rolling(window=50).mean()
    data["SMA200"] = data["Close"].rolling(window=200).mean()
    data["Signal"] = 0
    data["Signal"][50:] = data["SMA50"][50:] > data["SMA200"][50:]
    data["Position"] = data["Signal"].diff()
    data['Returns'] = data['Close'].pct_change()
    data['StrategyReturns'] = data['Returns'] * data['Position'].shift(1)
    data['CumulativeStrategyReturns'] = (1 + data['StrategyReturns']).cumprod() - 1
    data['CumulativeBuyHoldReturns'] = (1 + data['Returns']).cumprod() - 1
    return data
