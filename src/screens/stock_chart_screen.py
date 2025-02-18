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


class StockChartView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

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
        )

        self.graph_widget = BoxLayout(
            size_hint=(1, 0.8),
            padding=[15, 15, 15, 15],
        )

        self.add_widget(self.chart_label)
        self.add_widget(self.graph_widget)
        self.add_widget(self.back_button)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

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

        self.graph_widget.clear_widgets()
        self.graph_widget.add_widget(FigureCanvasKivyAgg(fig))


class StockChartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.view = StockChartView()
        self.view.back_button.on_press = self.go_back

        self.add_widget(self.view)

        stock_data = StockChartData.fetch_mock_data()
        self.view.update_graph(stock_data)

    def go_back(self):
        self.manager.current = "home"
