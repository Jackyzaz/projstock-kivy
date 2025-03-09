# screens/favorite_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from favorite_manager import FavoriteManager

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.auto_complete import fetch_stock_symbols


class FavoriteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical")

        # Search Input
        self.stock_symbols = fetch_stock_symbols()
        self.search_input = MDTextField(
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            hint_text="Enter stock symbol or company name (e.g., AAPL or Apple)",
            helper_text="Type to see suggestions",
            helper_text_mode="persistent",
        )
        self.search_input.bind(text=self.on_text)
        self.layout.add_widget(self.search_input)

        # Search Button
        self.search_button = MDRaisedButton(
            text="Search & Save", pos_hint={"center_x": 0.5}, on_release=self.add_stock
        )
        self.layout.add_widget(self.search_button)

        # Scrollable Favorite List
        self.scroll_view = MDScrollView()
        self.favorite_list = MDList()
        self.scroll_view.add_widget(self.favorite_list)
        self.layout.add_widget(self.scroll_view)

        self.add_widget(self.layout)
        self.load_favorites()

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
                    if value.lower() in symbol.lower() or (
                        company_name and value.lower() in company_name.lower()
                    ):
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

    def load_favorites(self):
        """Loads and displays favorite stocks."""
        self.favorite_list.clear_widgets()
        favorites = FavoriteManager.load_favorites()
        for stock in favorites:
            self.add_stock_item(stock)

    def add_stock_item(self, stock_code):
        """Adds a stock to the UI favorite list."""
        item = OneLineAvatarIconListItem(text=stock_code)
        icon = IconLeftWidget(icon="star")
        icon.bind(on_release=lambda x, s=stock_code: self.remove_favorite(s))
        item.add_widget(icon)
        self.favorite_list.add_widget(item)

    def add_stock(self, instance):
        """Adds a searched stock to the favorites list."""
        stock_code = self.search_input.text.strip().upper()

        if stock_code and stock_code not in FavoriteManager.load_favorites():
            FavoriteManager.add_favorite(stock_code)
            self.add_stock_item(stock_code)
            self.search_input.text = ""  # Clear input field after adding

    def remove_favorite(self, stock_code):
        """Removes a stock from favorites and refreshes the list."""
        FavoriteManager.remove_favorite(stock_code)
        self.load_favorites()
