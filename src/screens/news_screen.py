import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import plot_stock_data

from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from src.data.news_data import fetch_stock_news, fetch_stock_info
import webbrowser

from src.screens.favorite_manager import FavoriteManager  # Import FavoriteManager
from src.data.auto_complete import fetch_stock_symbols

Builder.load_file("NewsScreen.kv")


class StockInfo(MDBoxLayout):
    """Stock Information Overview"""

    stock_name = StringProperty()
    stock_fullname = StringProperty()
    stock_value = StringProperty()
    stock_change = StringProperty()
    stock_status = StringProperty()


class NewCard(MDCard):
    """Dynamically generated News Card"""

    title = StringProperty()
    description = StringProperty()
    source = StringProperty()
    time = StringProperty()
    click_through_url = StringProperty()

    def Push(self):
        """Open news link in a WebView window"""
        print(self.click_through_url)
        webbrowser.open(self.click_through_url)


class NewsScreen(MDScreen):
    """News Screen with Hot Reload Support"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_symbols = fetch_stock_symbols()
        Clock.schedule_once(self.get_stock_info, 1)  # Load initial stock data

    def get_stock_data(self, stock_id):
        """Fetch stock data and news separately and update UI"""
        print(f"Fetching stock data for: {stock_id}")

        stock_info = self.ids.get("stock_info", None)
        news_grid = self.ids.get("news_grid", None)

        if not stock_info or not news_grid:
            print("Error: stock_info or news_grid not found in KV file.")
            return

        # Clear old news before adding new ones
        news_grid.clear_widgets()

        # Fetch stock details
        stock_data = fetch_stock_info(stock_id.upper())

        # Fetch stock news
        news_data = fetch_stock_news(stock_id.upper())

        # Update stock UI
        stock_info.clear_widgets()
        stock_info.add_widget(
            StockInfo(
                stock_name=stock_data.get("stock_name", "N/A"),
                stock_fullname=stock_data.get("stock_fullname", "N/A"),
                stock_value=str(stock_data.get("stock_value", "N/A")),
                stock_change=str(stock_data.get("stock_change", "N/A")),
                stock_status=stock_data.get("stock_status", "N/A"),
            )
        )

        # Populate news UI
        for news in news_data:
            news_card = NewCard(
                source=news.get("provider", ""),
                title=news.get("title", "No title available"),
                description=news.get("summary", "No summary available"),
                time=news.get("pubDate", "Unknown date"),
                click_through_url=news.get("click_through_url", "Invalid Link"),
            )
            news_grid.add_widget(news_card)

    def get_stock_info(self, dt=None):
        """Load default stock information"""

        favorite_stocks = FavoriteManager.load_favorites()
        ticker = favorite_stocks[0] if favorite_stocks else "NVDA"

        stock_info = self.ids.get("stock_info", None)
        news_grid = self.ids.get("news_grid", None)

        if not stock_info or not news_grid:
            print("Error: stock_info or news_grid not found in KV file.")
            return

        # Fetch stock details
        stock_data = fetch_stock_info(ticker)

        # Fetch stock news
        news_data = fetch_stock_news(ticker)

        # Update stock UI
        stock_info.clear_widgets()
        stock_info.add_widget(
            StockInfo(
                stock_name=stock_data.get("stock_name", "N/A"),
                stock_fullname=stock_data.get("stock_fullname", "N/A"),
                stock_value=str(stock_data.get("stock_value", "N/A")),
                stock_change=str(stock_data.get("stock_change", "N/A")),
                stock_status=stock_data.get("stock_status", "N/A"),
            )
        )

        # Update news UI
        news_grid.clear_widgets()
        for news in news_data:
            news_card = NewCard(
                source=news.get("provider", ""),
                title=news.get("title", "No title available"),
                description=news.get("summary", "No summary available"),
                time=news.get("pubDate", "Unknown date"),
                click_through_url=news.get("click_through_url", "Unknown date"),
            )
            news_grid.add_widget(news_card)

    def populate_news(self, dt):
        """Populate the grid with news data"""
        news_grid = self.ids.get("news_grid", None)

        if not news_grid:
            print("Error: news_grid not found in KV file.")
            return

        # Clear previous news to avoid duplicates
        news_grid.clear_widgets()

        # Fetch default news initially
        for news in fetch_stock_news("default"):
            news_card = NewCard(
                source=news["source"],
                title=news["title"],
                description=news["description"],
                time=news["time"],
                click_through_url=news.get("click_through_url", "Unknown date"),
            )
            news_grid.add_widget(news_card)

    def auto_complete(self, instance, value):
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
                instance.helper_text = ", ".join(suggestions[:3])
            else:
                instance.helper_text = "No suggestions found"
        else:
            instance.helper_text = "Type to see suggestions"
