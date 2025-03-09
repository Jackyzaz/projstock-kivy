import sys
import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
import yfinance as yf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import plot_stock_data
from stock_utils import fetch_stock_symbols, handle_dropdown, update_dropdown, select_suggestion

class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_symbols = fetch_stock_symbols()
        if not self.stock_symbols:
            print("No stock symbols loaded, using default list")
            self.stock_symbols = [
                "AAPL (Apple Inc.)", "NVDA (NVIDIA Corporation)", "MSFT (Microsoft Corporation)",
                "GOOGL (Alphabet Inc.)", "TSLA (Tesla, Inc.)"
            ]
        
        print(f"Loaded {len(self.stock_symbols)} stock symbols: {self.stock_symbols[:5]}")

        self.main_layout = FloatLayout()
        
        self.layout = BoxLayout(
            orientation='vertical', 
            padding="20dp", 
            spacing="20dp",
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.search_input = MDTextField(
            hint_text="Enter stock symbol or company name (e.g., AAPL or Apple)",
            helper_text="Type to see suggestions",
            helper_text_mode="persistent",
            size_hint_y=None,
            height=dp(48),
            pos_hint={'top': 1}
        )
        self.search_input.bind(text=lambda instance, value: handle_dropdown(self, value, search_input=self.search_input, suggestion_list=self.suggestion_list, stock_symbols=self.stock_symbols), on_focus=self.on_focus)
        self.layout.add_widget(self.search_input)

        self.suggestion_list = MDList()
        self.layout.add_widget(self.suggestion_list)

        self.period_layout = BoxLayout(
            orientation='horizontal',
            spacing="5dp",
            size_hint_y=None,
            height=dp(40)
        )

        self.period_buttons = {}
        periods = ["1d", "5d", "1wk", "1mo", "6mo", "1y", "max"]
        self.selected_period = "1y"
        for period in periods:
            btn = MDRectangleFlatButton(
                text=period.upper(),
                size_hint=(None, 1),
                width=dp(60),
                md_bg_color=[0.2, 0.2, 0.2, 1] if period != self.selected_period else [0.4, 0.4, 0.4, 1],  # ไฮไลต์ปุ่มที่เลือก
                text_color=[1, 1, 1, 1]
            )
            btn.bind(on_press=lambda instance, p=period: self.update_period(p))
            self.period_buttons[period] = btn
            self.period_layout.add_widget(btn)
        self.layout.add_widget(self.period_layout)

        self.fetch_button = MDRaisedButton(
            text="Fetch Data",
            md_bg_color=(1, 0.34, 0.13, 1),
            on_press=self.fetch_data,
            size_hint_y=None,
            height=dp(48)
        )
        self.layout.add_widget(self.fetch_button)
        
        plt = plot_stock_data("NVDA", self.selected_period)
        if plt is None:
            self.show_error("Failed to load initial chart for NVDA")
            self.chart = FigureCanvasKivyAgg(plt.figure())  # สร้าง figure ว่างเพื่อหลีกเลี่ยงข้อผิดพลาด
        else:
            self.chart = FigureCanvasKivyAgg(plt.gcf())
        self.layout.add_widget(self.chart)
        
        self.main_layout.add_widget(self.layout)
        self.add_widget(self.main_layout)

        self.dialog = None
        self.current_symbol = "NVDA"
        self.is_dropdown_open = False
        self.selected_index = -1 
        self.suggestions = []  

        self.search_input.bind(
            size=self.update_dropdown_pos,
            pos=self.update_dropdown_pos
        )
        
        Window.bind(on_touch_down=lambda instance, value: handle_dropdown(self, value, search_input=self.search_input, suggestion_list=self.suggestion_list, stock_symbols=self.stock_symbols))
        Window.bind(on_key_down=lambda instance, value1, value2, value3, value4: handle_dropdown(self, keycode=value1, search_input=self.search_input, suggestion_list=self.suggestion_list, stock_symbols=self.stock_symbols))

    def update_dropdown_pos(self, instance, value):
        if hasattr(self.search_input, 'to_window'):
            x, y = self.search_input.to_window(self.search_input.x, self.search_input.y)
            if self.suggestion_list:  
                self.suggestion_list.pos = (x, y - self.suggestion_list.height)
            self.suggestion_list.width = self.search_input.width

    def on_focus(self, instance, value):
        if value and self.suggestions: 
            self.is_dropdown_open = True
            update_dropdown(self, self.suggestion_list, self.suggestions, self.selected_index)

    def update_period(self, period):
        self.selected_period = period
        for p, btn in self.period_buttons.items():
            btn.md_bg_color = [0.4, 0.4, 0.4, 1] if p == period else [0.2, 0.2, 0.2, 1]  # ไฮไลต์ปุ่มที่เลือก
        self.fetch_data(None)

    def fetch_data(self, instance):
        symbol = self.search_input.text.split(" (")[0] if "(" in self.search_input.text else self.search_input.text
        if not symbol:
            symbol = self.current_symbol 
        if not symbol:
            self.show_error("Please enter a stock symbol")
            return
        
        try:
            print(f"Fetching data for {symbol} with period={self.selected_period}") 
            plt = plot_stock_data(symbol, self.selected_period)
            if plt is None:
                self.show_error(f"Failed to fetch data for {symbol} with period={self.selected_period}")
                return
            self.current_symbol = symbol
            self.chart.figure = plt.gcf()
            self.chart.draw()
            self.is_dropdown_open = False
            self.suggestion_list.height = 0
        except Exception as e:
            self.show_error(f"Error fetching {symbol}: {e}")

    def show_error(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(
                text="OK",
                on_press=lambda x: self.dialog.dismiss()
            )]
        )
        self.dialog.open()