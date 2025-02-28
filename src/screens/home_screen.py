import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import get_data, get_multiple_data

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
import numpy as np
import matplotlib.pyplot as plt


class Home_ScreenApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        # ✅ โหลด UI และให้มันแสดงผลก่อน
        self.layout = Builder.load_file("HomeScreen.kv")

        # ✅ แสดงข้อความ "กำลังโหลดข้อมูล..." ก่อน
        self.loading_label = MDLabel(
            text="กำลังโหลดข้อมูล...", halign="center", theme_text_color="Secondary"
        )
        self.layout.ids.stock_table_box.add_widget(self.loading_label)

        return self.layout  # ✅ ให้ UI แสดงผลก่อนโหลดข้อมูล

    def on_start(self):
        # ✅ ใช้ Clock เพื่อให้ UI แสดงผลก่อน แล้วค่อยโหลดข้อมูลหลัง 0.5 วินาที
        Clock.schedule_once(self.start_loading, 0.5)

    def start_loading(self, *args):
        """เริ่มโหลดข้อมูลแบบ Async"""
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
        self.load_stock_data()  # ✅ โหลดข้อมูลก่อน

        # ✅ ตรวจสอบว่ามี stock_table_box หรือไม่
        if hasattr(self.root.ids, "stock_table_box"):
            self.root.ids.stock_table_box.clear_widgets()  # ✅ ลบข้อความ "กำลังโหลดข้อมูล..."
            self.root.ids.stock_table_box.add_widget(self.stock_table)  # ✅ เพิ่มตาราง
        else:
            print("Error: ไม่พบ stock_table_box ใน .kv")

    def get_color(self, value):
        """คืนค่าเป็นสีเขียวถ้าบวก, แดงถ้าลบ, และขาวถ้าเป็น 0"""
        try:
            value = float(value)
            if value > 0:
                return "00FF00"  # สีเขียว
            elif value < 0:
                return "FF0000"  # สีแดง
            else:
                return "FFFFFF"  # สีขาว
        except:
            return "FFFFFF"  # สีขาว กรณีผิดพลาด


Home_ScreenApp().run()
