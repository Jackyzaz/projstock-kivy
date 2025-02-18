from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt


class StockChartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.chart_label = Label(
            text="Stock Chart",
            font_size=58,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
        )

        self.back_button = Button(
            text="Back",
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.2, 0.2, 1),
            font_size=20,
            on_press=self.go_back,
        )

        self.graph_widget = BoxLayout(
            size_hint=(1, 0.5),
            padding=[15, 15, 15, 15],
        )

        self.layout.add_widget(self.chart_label)
        self.layout.add_widget(self.graph_widget)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)
        self.plot_candlestick_chart()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def go_back(self, instance):
        self.manager.current = "home"

    def plot_candlestick_chart(self):
        data = self.mock_fetch_stock_data()
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

        self.graph_widget.clear_widgets()
        self.graph_widget.add_widget(FigureCanvasKivyAgg(fig))

    def mock_fetch_stock_data(self):
        dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
        opens = np.random.uniform(100, 150, 30)
        closes = opens + np.random.uniform(-5, 5, 30)
        highs = np.maximum(opens, closes) + np.random.uniform(0, 5, 30)
        lows = np.minimum(opens, closes) - np.random.uniform(0, 5, 30)
        volumes = np.random.randint(1000, 5000, 30)

        df = pd.DataFrame(
            {
                "Open": opens,
                "High": highs,
                "Low": lows,
                "Close": closes,
                "Volume": volumes,
            },
            index=dates,
        )
        return df
