import threading
from kivy.uix.screenmanager import Screen
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.clock import Clock
import numpy as np
import pandas as pd
import mplfinance as mpf


class StockChartScreen(Screen):
    def on_enter(self):
        self.ids.graph_widget.opacity = 0
        self.ids.loading_label.opacity = 1
        ticker = getattr(self, "ticker", "AAPL")  # Default to "AAPL" if not set
        time_period = getattr(self, "time_period", "1d")
        self.load_stock_data(ticker, time_period)

    def load_stock_data(self, ticker, time_period):
        threading.Thread(
            target=self.update_chart, args=(ticker, time_period), daemon=True
        ).start()

    def update_chart(self, ticker, time_period):
        data = StockChartData.fetch_mock_data()
        Clock.schedule_once(lambda dt: self.update_ui(data, ticker, time_period))

    def update_ui(self, data, ticker, time_period):
        self.ids.chart_label.text = f"Stock Chart for {ticker} ({time_period})"
        self.update_graph(data)
        self.ids.loading_label.opacity = 0
        self.ids.graph_widget.opacity = 1

    def update_graph(self, data):
        if data is None or data.empty:
            return

        custom_style = mpf.make_mpf_style(
            base_mpf_style="nightclouds",
            marketcolors=mpf.make_marketcolors(
                up="green",
                down="red",
                edge="inherit",
                wick="white",
                volume="blue",
            ),
            figcolor="black",
            gridcolor="gray",
        )

        fig, axes = mpf.plot(
            data,
            type="candle",
            style=custom_style,
            ylabel="Price (USD)",
            volume=True,
            returnfig=True,
            figsize=(20, 10),
        )

        self.ids.graph_widget.clear_widgets()
        self.ids.graph_widget.add_widget(FigureCanvasKivyAgg(fig))

    def go_back(self):
        self.manager.current = "home"


class StockChartData:
    @staticmethod
    def fetch_mock_data():

        dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
        opens = np.random.uniform(100, 150, 30)
        closes = opens + np.random.uniform(-5, 5, 30)
        highs = np.maximum(opens, closes) + np.random.uniform(0, 5, 30)
        lows = np.minimum(opens, closes) - np.random.uniform(0, 5, 30)
        volumes = np.random.randint(1000, 5000, 30)

        return pd.DataFrame(
            {
                "Open": opens,
                "High": highs,
                "Low": lows,
                "Close": closes,
                "Volume": volumes,
            },
            index=dates,
        )
