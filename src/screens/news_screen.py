from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

MOCK_STOCK_INFO = {
    "stock_name": "Dow Jones",
    "stock_fullname": "Dow Jones Industrial Average",
    "stock_value": "43,428.02",
    "stock_change": "-748.63",
    "stock_status": "Market Closed",
}

MOCK_NEWS_DATA = [
    {
        "source": "finance.com",
        "title": "Stock Market Hits New High",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "2 hours ago",
    },
    {
        "source": "businessnews.com",
        "title": "Tech Giants Report Record Profits",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "5 hours ago",
    },
    {
        "source": "energywatch.com",
        "title": "Oil Prices Surge Amid Global Tensions",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "8 hours ago",
    },
    {
        "source": "cryptoalert.com",
        "title": "Cryptocurrency Market Sees Volatility",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "1 day ago",
    },
    {
        "source": "cryptoalert.com",
        "title": "Cryptocurrency Market Sees Volatility",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "1 day ago",
    },
    {
        "source": "cryptoalert.com",
        "title": "Cryptocurrency Market Sees Volatility",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "1 day ago",
    },
    {
        "source": "finance.com",
        "title": "Stock Market Hits New High",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "2 hours ago",
    },
    {
        "source": "businessnews.com",
        "title": "Tech Giants Report Record Profits",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "5 hours ago",
    },
    {
        "source": "energywatch.com",
        "title": "Oil Prices Surge Amid Global Tensions",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "8 hours ago",
    },
    {
        "source": "cryptoalert.com",
        "title": "Cryptocurrency Market Sees Volatility",
        "description": "Description on the description with description after description before description. Description on the description with description after description before description",
        "time": "1 day ago",
    },
]


class StockInfo(MDBoxLayout):
    """Stock Infomation Overview"""

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


class NewsScreen(MDScreen):
    """News Screen with Hot Reload Support"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.populate_news, 0.1)
        Clock.schedule_once(self.get_stock_info, 0.1)  # Ensure ids are loaded

    def get_stock_info(self, dt):
        stock_info = self.ids.get("stock_info", None)  # Use correct ID
        if not stock_info:
            print("Error: stock_info not found in KV file.")
            return
        stock_info.clear_widgets()
        stock_info.add_widget(
            StockInfo(
                stock_name=MOCK_STOCK_INFO["stock_name"],
                stock_fullname=MOCK_STOCK_INFO["stock_fullname"],
                stock_value=MOCK_STOCK_INFO["stock_value"],
                stock_change=MOCK_STOCK_INFO["stock_change"],
                stock_status=MOCK_STOCK_INFO["stock_status"],
            )
        )

    def populate_news(self, dt):
        """Populate the grid with mock data"""
        news_grid = self.ids.get("news_grid", None)

        if not news_grid:
            print("Error: news_grid not found in KV file.")
            return

        news_grid.clear_widgets()

        for news in MOCK_NEWS_DATA:
            news_card = NewCard(
                source=news["source"],
                title=news["title"],
                description=news["description"],
                time=news["time"],
            )
            news_grid.add_widget(news_card)
