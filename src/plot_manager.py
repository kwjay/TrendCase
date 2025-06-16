import matplotlib.pyplot as plt
import pandas as pd

class PlotManager:
    def __init__(self, df: pd.DataFrame) -> None:
        self.data = df

    def plot_price(self, axes=None) -> None:
        axes = axes or plt.gca()
        axes.plot(self.data.index, self.data["close"], label="Close", color="black")
        axes.set_title(label="Close Price")
        axes.legend()

    def plot_sma_crossover(self, fast: int, slow: int, axes=None) -> None:
        axes = axes or plt.gca()
        axes.plot(self.data.index, self.data["close"], label="Close", color="black", alpha=0.5)
        axes.plot(self.data.index, self.data[f"sma{fast}"], label=f"sma{fast}")
        axes.plot(self.data.index, self.data[f"sma{slow}"], label=f"sma{slow}")
        axes.set_title(f"SMA {fast}/{slow} Crossover")
        axes.legend()

    def plot_rsi(self, period: int, lower: float, upper: float, axes=None) -> None:
        axes = axes or plt.gca()
        axes.plot(self.data.index, self.data[f"RSI{period}"], label=f"RSI{period}")
        axes.axhline(lower, linestyle='--', color='red', label=f"Lower {lower}")
        axes.axhline(upper, linestyle='--', color='green', label=f"Upper {upper}")
        axes.set_ylim(0, 100)
        axes.set_title(f"RSI ({period})")
        axes.legend()

    def show(self) -> None:
        plt.tight_layout()
        plt.show()