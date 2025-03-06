import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.Data.stock_data import get_multiple_data
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
import yfinance as yf
from datetime import datetime
import pandas as pd
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard



def fetch_stock_news(tickers=None):
    """ดึงข่าวจาก yfinance ของหลายหุ้น"""
    if tickers is None:
        tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "NVDA"]

    formatted_news = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            news_list = stock.get_news()
        except Exception:
            formatted_news.append(
                {
                    "ticker": ticker,
                    "title": "Failed to Load News",
                    "summary": "Please try again.",
                    "pubDate": "-",
                }
            )
            continue

        if not news_list:
            formatted_news.append(
                {
                    "ticker": ticker,
                    "title": "No News Available",
                    "summary": "No recent news found.",
                    "pubDate": "-",
                }
            )
            continue

        for news in news_list[:3]:
            content = news.get("content", {})
            title = content.get("title", "No Title")
            summary = content.get("summary", "No Summary")
            pubDate = content.get("pubDate", "-")

            try:
                dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
            except:
                formatted_date = "Unknown Date"

            formatted_news.append(
                {
                    "ticker": ticker,
                    "title": title,
                    "summary": summary,
                    "pubDate": formatted_date,
                }
            )

    return formatted_news


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_data = []

    def on_start(self):
        Clock.schedule_once(self.show_loading_label, 0)
        Clock.schedule_once(self.show_news_loading_label, 0)
        Clock.schedule_once(self.start_loading, 0.5)
        Clock.schedule_once(self.load_latest_news, 1)
        Clock.schedule_interval(self.update_datetime, 1)

    def update_datetime(self, dt):
        """อัปเดตวันที่และเวลาใน Stock Box"""
        if hasattr(self.root.ids, "stock_datetime"):
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.root.ids.stock_datetime.text = f"Updated: {now}"

    def show_loading_label(self, *args):
        """แสดง 'Loading stock data...'"""
        if hasattr(self.root.ids, "stock_table_box"):
            self.root.ids.stock_table_box.clear_widgets()
            self.loading_label = MDLabel(
                text="Loading stock data...",
                halign="center",
                theme_text_color="Secondary",
                font_style="H5",
            )
            self.root.ids.stock_table_box.add_widget(self.loading_label)

    def start_loading(self, *args):
        """เริ่มโหลดข้อมูล"""
        Clock.schedule_once(self.update_stock_table, 0)

    def load_stock_data(self):
        """โหลดข้อมูลหุ้น"""
        stock_list = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NFLX", "NVDA", "BABA"]
        try:
            stock_data = get_multiple_data(stock_list, "5d", "1h")
        except Exception:
            self.row_data = [("Failed to Load Data", "-", "-", "-", "-", "-", "-")]
            return

        if not stock_data:
            self.row_data = [("No Stock Data Available", "-", "-", "-", "-", "-", "-")]
            return

        self.row_data = []
        for stock, data in stock_data.items():
            if data.empty:
                continue

            latest_data = data.iloc[-1]  # latest_data คือล่าสุดของ DataFrame

            try:
                high = latest_data["High"]
                low = latest_data["Low"]
                close = latest_data["Close"]
                open_price = latest_data["Open"]

                # ถ้าเป็น Series (มีแค่ 1 ค่า), ใช้ .item() เพื่อดึงค่ามาเป็น float
                if isinstance(high, pd.Series):
                    high = high.item()
                if isinstance(low, pd.Series):
                    low = low.item()
                if isinstance(close, pd.Series):
                    close = close.item()
                if isinstance(open_price, pd.Series):
                    open_price = open_price.item()

            except KeyError:
                continue

            change = close - open_price
            gain = (change / open_price) * 100 if open_price != 0 else 0

            close_prices = data["Close"].dropna()
            if len(close_prices) > 1:
                start_price = close_prices.iloc[0]

                # เช็คและแปลงค่า start_price เหมือนกัน
                if isinstance(start_price, pd.Series):
                    start_price = start_price.item()

                avg_return = ((close - start_price) / start_price) * 100
            else:
                avg_return = 0.00

            self.row_data.append(
                (
                    stock,
                    f"${high:.2f}",
                    f"${low:.2f}",
                    f"${close:.2f}",
                    f"[color={self.get_color(change)}]{change:.2f}[/color]",
                    f"[color={self.get_color(gain)}]{gain:.2f}%[/color]",
                    f"[color={self.get_color(avg_return)}]{avg_return:.2f}%[/color]",
                )
            )

        if not self.row_data:
            self.row_data = [("No Stock Data Available", "-", "-", "-", "-", "-", "-")]

        self.stock_table = MDDataTable(
            background_color_header="#000000",
            rows_num=len(self.row_data),
            size_hint=(1, None),
            height=dp(50) * (len(self.row_data) + 2),
            pos_hint={"center_x": 0.5},
            column_data=[("Company Name", dp(50)),
                         ("High", dp(38)),
                         ("Low", dp(38)),
                         ("Prev Close", dp(43)),
                         ("Change", dp(43)),
                         ("Gain", dp(43)),
                         ("5 Day Avg", dp(48))],
            row_data=self.row_data,
        )

    def update_stock_table(self, *args):
        """อัปเดตตารางหุ้น"""
        self.load_stock_data()
        Clock.schedule_once(self.replace_table, 0.2)

    def replace_table(self, *args):
        """แทนที่ loading ด้วยตาราง"""
        if hasattr(self.root.ids, "stock_table_box"):
            self.root.ids.stock_table_box.clear_widgets()
            self.root.ids.stock_table_box.add_widget(self.stock_table)

    def show_news_loading_label(self, *args):
        """แสดงข้อความ 'Loading news...' ก่อนโหลดข่าว"""
        if hasattr(self.root.ids, "latest_news_box"):
            self.loading_news_label = MDLabel(
                text="Loading news...",
                halign="center",
                theme_text_color="Secondary",
                font_style="H5",
            )
            self.root.ids.latest_news_box.clear_widgets()
            self.root.ids.latest_news_box.add_widget(self.loading_news_label)

        Clock.schedule_once(self.load_latest_news, 1)

    def load_latest_news(self, *args):
        """โหลดข่าวและแสดงให้เต็ม latest_news_box"""
        news_data = fetch_stock_news(["AAPL", "MSFT", "TSLA", "AMZN", "NVDA"])
        if not hasattr(self.root.ids, "latest_news_box"):
            print("Error: latest_news_box ไม่พบใน .kv")
            return

        latest_news_box = self.root.ids.latest_news_box
        latest_news_box.clear_widgets()

        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
        )

        news_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            adaptive_height=True,
        )

        for news in news_data:
            news_card = MDCard(
                size_hint_x=1,
                size_hint_y=None,
                height=dp(120),
                padding=dp(10),
                md_bg_color=(0.2, 0.2, 0.2, 1),
                radius=[10],
                elevation=5,
            )

            news_box = MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                padding=(dp(10), dp(5)),
            )

            title_label = MDLabel(
                text=news["title"],
                font_style="H6",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(30),
                shorten=True,
                shorten_from="right",
            )

            summary_label = MDLabel(
                text=news["summary"],
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(50),
                max_lines=3,
                shorten=True,
                shorten_from="right",
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

    def get_color(self, value):
        """คืนค่าเป็นสีเขียวถ้าบวก, แดงถ้าลบ, และขาวถ้าเป็น 0"""
        try:
            value = float(value)
            return "00FF00" if value > 0 else "FF0000"
        except:
            return "FFFFFF"

    def refresh_data(self):
        """โหลดข้อมูลใหม่และแสดง Loading"""
        self.show_loading_label()
        self.show_news_loading_label()
        Clock.schedule_once(self.update_stock_table, 1)
        Clock.schedule_once(
            lambda dt: self.load_latest_news(["AAPL", "MSFT", "TSLA", "AMZN", "NVDA"]),
            1,
        )
