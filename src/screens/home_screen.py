import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import get_multiple_data
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
import yfinance as yf
from datetime import datetime
from kivy.uix.scrollview import ScrollView


def fetch_stock_news(ticker="NVDA"):
    """ดึงข่าวจาก yfinance"""
    stock = yf.Ticker(ticker)
    news_list = stock.get_news()

    if not news_list:
        return []

    formatted_news = []
    for news in news_list[:4]:
        content = news.get("content", {})
        title = content.get("title", "No Title")
        summary = content.get("summary", "No Summary")
        pubDate = content.get("pubDate", "")

        try:
            dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
        except:
            formatted_date = "Unknown Date"

        formatted_news.append(
            {"title": title, "summary": summary, "pubDate": formatted_date}
        )

    return formatted_news


class Home_ScreenApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.layout = Builder.load_file("HomeScreen.kv")
        return self.layout

    def on_start(self):
        Clock.schedule_once(self.show_loading_label, 0)
        Clock.schedule_once(self.start_loading, 0.5)
        Clock.schedule_once(self.load_latest_news, 1)

    def show_loading_label(self, *args):
        """แสดงข้อความ 'กำลังโหลดข้อมูล...'"""
        if hasattr(self.root.ids, "stock_table_box"):
            self.loading_label = MDLabel(
                text="Loading stock data...",
                halign="center",
                theme_text_color="Secondary",
                font_style="H5",
            )
            self.root.ids.stock_table_box.clear_widgets()
            self.root.ids.stock_table_box.add_widget(self.loading_label)

    def start_loading(self, *args):
        """เริ่มโหลดข้อมูลหลังจาก 0.5 วินาที"""
        Clock.schedule_once(self.update_stock_table, 0)

    def load_stock_data(self):
        """โหลดข้อมูลหุ้น"""
        stock_list = [
            "AAPL",
            "GOOGL",
            "MSFT",
            "AMZN",
            "TSLA",
            "NFLX",
            "NVDA",
            "FB",
            "BABA",
        ]
        stock_data = get_multiple_data(stock_list, "5d", "1h")

        self.row_data = []
        for stock, data in stock_data.items():
            latest_data = data.iloc[-1]
            close_prices = data["Close"].dropna()

            if len(close_prices) > 1:
                start_price = close_prices.iloc[0].item()
                end_price = close_prices.iloc[-1].item()
                avg_return = ((end_price - start_price) / start_price) * 100
            else:
                avg_return = 0.00

            change = latest_data["Close"].iloc[0] - latest_data["Open"].iloc[0]
            gain = (change / latest_data["Open"].iloc[0]) * 100

            self.row_data.append(
                (
                    stock,
                    f"${latest_data['High'].iloc[0]:.2f}",
                    f"${latest_data['Low'].iloc[0]:.2f}",
                    f"${latest_data['Close'].iloc[0]:.2f}",
                    f"[color={self.get_color(change)}]{change:.2f}[/color]",
                    f"[color={self.get_color(gain)}]{gain:.2f}%[/color]",
                    f"[color={self.get_color(avg_return)}]{avg_return:.2f}%[/color]",
                )
            )

        self.stock_table = MDDataTable(
            background_color_header="#000000",
            rows_num=len(self.row_data),
            size_hint=(1, None),
            height=dp(50) * (len(self.row_data) + 2),
            pos_hint={"center_x": 0.5},
            column_data=[
                ("Company Name", dp(50)),
                ("High", dp(38)),
                ("Low", dp(38)),
                ("Prev Close", dp(43)),
                ("Change", dp(43)),
                ("Gain", dp(43)),
                ("5 Day Avg", dp(48)),
            ],
            row_data=self.row_data,
        )

    def update_stock_table(self, *args):
        """อัปเดตตารางหุ้น"""
        self.load_stock_data()
        Clock.schedule_once(self.replace_table, 0.2)

    def replace_table(self, *args):
        """แทนที่ข้อความ 'กำลังโหลดข้อมูล...' ด้วยตาราง"""
        if hasattr(self.root.ids, "stock_table_box"):
            self.root.ids.stock_table_box.clear_widgets()
            self.root.ids.stock_table_box.add_widget(self.stock_table)

    def load_latest_news(self, *args):
        """โหลดข่าวและแสดงให้เต็ม latest_news_box"""
        news_data = fetch_stock_news()
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
                adaptive_height=True,
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


Home_ScreenApp().run()
