from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

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
        Clock.schedule_once(self.populate_news, 0.1)  # Ensure ids are loaded

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
