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
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
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
        self.search_input.bind(text=self.on_text)
        self.layout.add_widget(self.search_input)
        
        self.suggestion_card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            width=self.search_input.width,
            elevation=2,
            radius=[0, 0, 4, 4],
            padding=0,
            md_bg_color=[0.97, 0.97, 0.97, 1],  
            height=0, 
            opacity=0.95, 
        )
        self.suggestion_list = MDList()
        self.suggestion_card.add_widget(self.suggestion_list)
        
        self.fetch_button = MDRaisedButton(
            text="Fetch Data",
            md_bg_color=(1, 0.34, 0.13, 1),
            on_press=self.fetch_data,
            size_hint_y=None,
            height=dp(48)
        )
        self.layout.add_widget(self.fetch_button)
        
        plt = plot_stock_data("NVDA", "1y", "1d")
        self.chart = FigureCanvasKivyAgg(plt.gcf())
        self.layout.add_widget(self.chart)
        
        self.main_layout.add_widget(self.layout)
        self.add_widget(self.main_layout)
        
        self.main_layout.add_widget(self.suggestion_card)
        
        self.dialog = None
        self.current_symbol = "NVDA"
        
        self.search_input.bind(
            size=self.update_dropdown_pos,
            pos=self.update_dropdown_pos
        )
        
        Window.bind(on_touch_down=self.close_dropdown_if_outside)

    def update_dropdown_pos(self, instance, value):
        if hasattr(self.search_input, 'to_window'):
            x, y = self.search_input.to_window(self.search_input.x, self.search_input.y)
            self.suggestion_card.pos = (x, y - self.suggestion_card.height)
            self.suggestion_card.width = self.search_input.width

    def fetch_stock_symbols(self):

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

        print(f"Text input: {value}")
        self.suggestion_list.clear_widgets()
        
        if value and len(value) >= 2: 
            suggestions = []
            
            for stock in self.stock_symbols:
                try:
                    symbol = stock.split(" (")[0]
                    company_name = stock.split(" (")[1][:-1] if " (" in stock else ""
                    
                    exact_match = value.lower() in symbol.lower() or (company_name and value.lower() in company_name.lower())
                    
                    symbol_score = fuzz.partial_ratio(value.lower(), symbol.lower())
                    company_score = fuzz.partial_ratio(value.lower(), company_name.lower()) if company_name else 0
                    
                    score = max(symbol_score, company_score)
                    if exact_match:
                        score += 50
                        
                    if score > 70: 
                        suggestions.append((stock, score))
                        
                except Exception as e:
                    print(f"Error processing stock {stock}: {e}")
                    continue
            
            suggestions.sort(key=lambda x: x[1], reverse=True)
            
            max_suggestions = min(5, len(suggestions))
            if max_suggestions > 0:
                print(f"Top suggestions: {suggestions[:max_suggestions]}")
                
                for i in range(max_suggestions):
                    stock_item = suggestions[i][0]
                    item = OneLineListItem(
                        text=stock_item,
                        on_press=lambda x, s=stock_item: self.select_suggestion(s),
                        bg_color=[0.98, 0.98, 0.98, 1], 
                        theme_text_color="Custom",
                        text_color=[0, 0, 0, 0.87], 
                        divider="Full" 
                    )
                    self.suggestion_list.add_widget(item)
                
                self.suggestion_card.height = dp(48) * max_suggestions
                self.update_dropdown_pos(None, None)
            else:
                self.suggestion_card.height = 0
        else:
            self.suggestion_card.height = 0

    def select_suggestion(self, suggestion):

        self.search_input.text = suggestion
        self.suggestion_card.height = 0

    def close_dropdown_if_outside(self, instance, touch):
        if touch.button == 'left':
            if self.suggestion_card.height > 0: 
                if not self.suggestion_card.collide_point(*touch.pos) and not self.search_input.collide_point(*touch.pos):
                    self.suggestion_card.height = 0
                    return True

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
            self.suggestion_card.height = 0
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