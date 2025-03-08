import sys
import os
import csv
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from fuzzywuzzy import fuzz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import plot_stock_data

class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_symbols = self.fetch_stock_symbols()
        if not self.stock_symbols:
            print("No stock symbols loaded, using default list")
            self.stock_symbols = [
                "AAPL (Apple Inc.)", "NVDA (NVIDIA Corporation)", "MSFT (Microsoft Corporation)",
                "GOOGL (Alphabet Inc.)", "TSLA (Tesla, Inc.)"
            ]
        
        print(f"Loaded {len(self.stock_symbols)} stock symbols: {self.stock_symbols[:5]}")

        self.layout = BoxLayout(orientation='vertical', padding="20dp", spacing="20dp")
        
        self.search_input = MDTextField(
            hint_text="Enter stock symbol or company name (e.g., AAPL or Apple)",
            helper_text="Type to see suggestions",
            helper_text_mode="persistent"
        )
        self.search_input.bind(text=self.on_text) 
        self.layout.add_widget(self.search_input)
        
        self.fetch_button = MDRaisedButton(
            text="Fetch Data",
            md_bg_color=(1, 0.34, 0.13, 1),
            on_press=self.fetch_data
        )
        self.layout.add_widget(self.fetch_button)
        
        plt = plot_stock_data("NVDA", "1y", "1d")
        self.chart = FigureCanvasKivyAgg(plt.gcf())
        self.layout.add_widget(self.chart)
        
        self.add_widget(self.layout)
        self.dialog = None
        self.current_symbol = "NVDA"

    def fetch_stock_symbols(self):
        """
        อ่านสัญลักษณ์หุ้นจากไฟล์ CSV
        """
        stock_file = os.path.join(os.path.dirname(__file__), "stocks.csv")
        stock_list = []
        try:
            with open(stock_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) >= 2:
                        symbol, company = row[0], row[1]
                        stock_list.append(f"{symbol} ({company})")
            return stock_list
        except FileNotFoundError:
            print("stocks.csv not found, using default list")
            return []
        except Exception as e:
            print(f"Error reading stocks.csv: {e}")
            return []

    def on_text(self, instance, value):
        """
        ฟังก์ชัน Auto Complete (case-insensitive)
        ค้นหาทั้ง symbol และ company
        """
        print(f"Text input: {value}")
        if value:
            suggestions = []
            for stock in self.stock_symbols:
                try:
                    symbol = stock.split(" (")[0]
                    company_name = stock.split(" (")[1][:-1] if " (" in stock else ""
                    if value.lower() in symbol.lower() or (company_name and value.lower() in company_name.lower()):
                        suggestions.append(stock)
                    elif company_name:
                        company_words = company_name.split()
                        if any(value.lower() in word.lower() for word in company_words):
                            suggestions.append(stock)
                except Exception as e:
                    print(f"Error processing stock {stock}: {e}")
                    continue
            if suggestions:
                print(f"Suggestions found: {suggestions[:3]}")
                self.search_input.helper_text = ", ".join(suggestions[:3]) 
            else:
                self.search_input.helper_text = "No suggestions found"
        else:
            self.search_input.helper_text = "Type to see suggestions"

    def fetch_data(self, instance):
        symbol = self.search_input.text.split(" (")[0] if "(" in self.search_input.text else self.search_input.text
        if not symbol:
            self.show_error("Please enter a stock symbol")
            return
        
        try:
            plt = plot_stock_data(symbol, "1y", "1d")
            self.current_symbol = symbol
            self.chart.figure = plt.gcf()
            self.chart.draw()
        except Exception as e:
            self.show_error(f"Error fetching {symbol}: {e}")

    def show_error(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_press=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
