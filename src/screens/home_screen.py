import sys
import os
from datetime import datetime
import pandas as pd
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.card import MDCard

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import get_multiple_data
from src.data.news_data import fetch_stock_news

KV_PATH = os.path.join(os.path.dirname(__file__), "HomeScreen.kv")
Builder.load_file(KV_PATH)


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_data = None
        self.news_data = None
        self.stock_table = None
        self.row_data = []

    def on_pre_enter(self):
        Clock.schedule_interval(self.update_datetime, 1)
        Clock.schedule_once(self.load_data, 0)

    def load_data(self, *args):
        if self.stock_data is None:
            self.show_loading_label("stock_table_box", "Loading stock data...")
            Clock.schedule_once(self.fetch_stock_data, 0.2)

        if self.news_data is None:
            self.show_loading_label("latest_news_box", "Loading news...")
            Clock.schedule_once(self.fetch_news_data, 0.2)

    def fetch_stock_data(self, *args):
        stock_list = [
            "AAPL",
            "GOOGL",
            "MSFT",
            "AMZN",
            "TSLA",
            "NFLX",
            "NVDA",
            "META",
        ]
        self.stock_data = get_multiple_data(stock_list, "5d", "1d")
        self.update_stock_table()

    def fetch_news_data(self, ticker="NVDA", *args):
        if not isinstance(ticker, str):
            ticker = "NVDA"
        self.news_data = fetch_stock_news(ticker)
        if hasattr(self, "show_latest_news"):
            self.show_latest_news(self)

    def show_latest_news(self, *args):
        if not self.news_data:
            return

        latest_news_box = self.ids.get("latest_news_box")
        if not latest_news_box:
            return

        latest_news_box.clear_widgets()

        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
        )
        news_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            adaptive_height=True,
            md_bg_color=(0.1, 0.1, 0.1, 1),
        )

        for news in self.news_data:
            news_card = MDCard(
                size_hint_x=1,
                size_hint_y=None,
                height=dp(120),
                md_bg_color=(0.1, 0.1, 0.1, 1),
            )
            news_box = MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                adaptive_height=True,
                md_bg_color=(0.1, 0.1, 0.1, 1),
            )

            title_label = MDLabel(
                text=news["title"],
                font_style="H6",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(30),
                shorten=True,
            )
            summary_label = MDLabel(
                text=news["summary"],
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(50),
                max_lines=3,
                shorten=True,
            )
            date_label = MDLabel(
                text=news["pubDate"],
                theme_text_color="Hint",
                size_hint_y=None,
                height=dp(20),
                font_style="Caption",
            )

            news_box.add_widget(title_label)
            news_box.add_widget(summary_label)
            news_box.add_widget(date_label)
            news_card.add_widget(news_box)
            news_layout.add_widget(news_card)

        scroll_view.add_widget(news_layout)
        latest_news_box.add_widget(scroll_view)

    def update_stock_table(self, *args):
        if not self.stock_data:
            return

        self.row_data = []
        for stock, data in self.stock_data.items():
            if data is None or data.empty:
                continue

            latest = data.iloc[-1]
            close_prices = data["Close"].dropna()

            if len(close_prices) > 1:
                start_price, end_price = close_prices.iloc[0], close_prices.iloc[-1]
                avg_return = ((end_price - start_price) / start_price) * 100
            else:
                avg_return = 0.00

            change = latest["Close"] - latest["Open"]
            gain = (change / latest["Open"]) * 100

            self.row_data.append(
                (
                    stock,
                    f"${latest['High']:.2f}",
                    f"${latest['Low']:.2f}",
                    f"${latest['Close']:.2f}",
                    self.format_value(change),
                    self.format_value(gain),
                    self.format_value(avg_return),
                )
            )

        self.stock_table = MDDataTable(
            background_color_header=(0.1, 0.1, 0.1, 1),
            background_color_cell=(0.1, 0.1, 0.1, 1),
            rows_num=len(self.row_data),
            size_hint=(1, None),
            height=dp(50) * (len(self.row_data) + 2),
            pos_hint={"center_x": 0.5},
            column_data=[
                ("Company", dp(50)),
                ("High", dp(38)),
                ("Low", dp(38)),
                ("Close", dp(43)),
                ("Change", dp(43)),
                ("Gain", dp(43)),
                ("5-Day Avg", dp(48)),
            ],
            row_data=self.row_data,
        )
        self.replace_widget("stock_table_box", self.stock_table)

    def update_datetime(self, dt):
        if hasattr(self.ids, "stock_datetime"):
            self.ids.stock_datetime.text = (
                f"Updated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

    def show_loading_label(self, widget_id, text):
        if hasattr(self.ids, widget_id):
            self.replace_widget(
                widget_id,
                MDLabel(
                    text=text,
                    halign="center",
                    theme_text_color="Secondary",
                    font_style="H5",
                ),
            )

    def replace_widget(self, widget_id, new_widget):
        if hasattr(self.ids, widget_id):
            self.ids[widget_id].clear_widgets()
            self.ids[widget_id].add_widget(new_widget)

    @staticmethod
    def format_value(value):
        if isinstance(value, pd.Series):
            value = value.iloc[0]
        return f"[color={'00FF00' if value > 0 else 'FF0000' if value < 0 else 'FFFFFF'}]{value:.2f}%[/color]"

    def refresh_data(self):
        self.stock_data = self.news_data = self.stock_table = None
        self.load_data()
