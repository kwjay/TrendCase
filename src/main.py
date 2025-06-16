import matplotlib.pyplot as plt

from trendcase_app import TrendCaseApp
from market_data import get_daily, load_daily
from plot_manager import PlotManager
from strategies import sma_crossover, rsi_threshold


if __name__ == "__main__":
    app = TrendCaseApp()
    app.run()
    # df = daily = load_daily("IBM", "data")
    # df = sma_crossover(df)
    # df = rsi_threshold(df)
    # print(df["RSI14"].describe())
    # plotter = PlotManager(df)
    #
    # figure, axes = plt.subplots(3,1, figsize=(12,8), sharex=True)
    # plotter.plot_price(axes=axes[0])
    # plotter.plot_sma_crossover(fast=50, slow=200, axes=axes[1])
    # plotter.plot_rsi(period=14, lower=30, upper=70, axes=axes[2])
    # plotter.show()


