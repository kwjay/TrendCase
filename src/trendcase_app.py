import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import market_data


class TrendCaseApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.status = tk.StringVar()
        self.api_key = tk.StringVar()
        self.symbol = tk.StringVar()
        self.df: pd.DataFrame | None = None

        self.title("TrendCase")
        self.geometry(f"{680}x{320}")
        self.resizable(False, False)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.axes = None
        self.canvas = None
        self.figure = Figure(figsize=(8, 5), dpi=100)

        self.create_controls()
        self.create_plot_canvas()

    def create_controls(self) -> None:
        frame = ttk.Frame(self, padding=10)
        frame.grid(row=0, column=0, sticky="ns")
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Alpha Vantage API key:").grid(sticky="w")
        api_entry = ttk.Entry(frame, textvariable=self.api_key, width=30)
        api_entry.grid(pady=(0, 10), sticky="ew")

        ttk.Label(frame, text="Symbol:").grid(sticky="w")
        symbol_entry = ttk.Entry(frame, textvariable=self.symbol, width=16)
        symbol_entry.grid(pady=(0, 10), sticky="ew")

        ttk.Separator(frame).grid(sticky="ew", pady=8)
        buttons = [
            ("Plot price", self.on_plot_price),
            ("Plot SMA", self.on_plot_sma),
            ("Plot RSI", self.on_plot_rsi),
            ("Plot GPT signal", self.on_plot_gpt),
        ]
        for txt, cmd in buttons:
            ttk.Button(frame, text=txt, command=cmd).grid(sticky="ew", pady=2)

        ttk.Separator(frame).grid(sticky="ew", pady=8)

        style = ttk.Style()
        style.configure("Compare.TButton", font=("Segoe UI", 10, "bold"), foreground="#A31621")
        ttk.Button(
            frame,
            text="Compare returns",
            style="Compare.TButton",
            command=self.on_compare_returns
        ).grid(sticky="ew", pady=2)

        ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w").grid(
            row=1, column=0, columnspan=2, sticky="ew"
        )

    def create_plot_canvas(self) -> None:
        frame = ttk.Frame(self)
        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.axes = self.figure.add_subplot(111)
        self.axes.set_title("Compare Returns", fontsize=16)
        self.axes.set_ylabel("Cumulative Return (%)")
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def get_api_key(self) -> bool:
        key = self.api_key.get().strip()
        if not key:
            messagebox.showwarning("Missing key", "Please enter your Alpha Vantage API key first.")
            return False
        market_data.API_KEY = key
        return True

    def get_symbol(self) -> str | None:
        symbol = self.symbol.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Missing ticker", "Please enter a symbol, e.g. SPY or IBM.")
            return None
        return symbol

    def load_data(self) -> pd.DataFrame | None:
        symbol = self.get_symbol()
        if symbol is None or not self.get_api_key():
            return None
        try:
            self.status.set(f"Fetching daily bars for {symbol}…")
            self.update_idletasks()
            df = market_data.get_daily(symbol)
            self.status.set(f"{len(df)} observations loaded for {symbol}, last bar {df.index.max().date()}")
            self.df = df
            return df
        except Exception as e:
            messagebox.showerror("Data error", f"Could not download data for {symbol}:\n{e}")
            self.status.set("Error")
            return None

    def on_plot_price(self) -> None:
        self.status.set("Plotting prices...")

    def on_plot_sma(self) -> None:
        self.status.set("Plotting SMA...")

    def on_plot_rsi(self) -> None:
        self.status.set("Plotting RSI...")

    def on_plot_gpt(self) -> None:
        self.status.set("Plotting GPT signals...")

    def on_compare_returns(self) -> None:
        self.status.set("Comparing returns...")

    def run(self) -> None:
        self.mainloop()