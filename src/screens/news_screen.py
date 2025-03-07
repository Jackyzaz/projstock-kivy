from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

MOCK_NEWS_DATA = [
    {
        "title": "Stock Market Hits New High",
        "description": "Description on the description with description after description before description",
        "source": "finance.com",
        "time": "2 hours ago",
    },
    {
        "title": "Tech Giants Report Record Profits",
        "description": "Description on the description with description after description before description",
        "source": "businessnews.com",
        "time": "5 hours ago",
    },
    {
        "title": "Oil Prices Surge Amid Global Tensions",
        "description": "Description on the description with description after description before description",
        "source": "energywatch.com",
        "time": "8 hours ago",
    },
    {
        "title": "Cryptocurrency Market Sees Volatility",
        "description": "Description on the description with description after description before description",
        "source": "cryptoalert.com",
        "time": "1 day ago",
    },
]


class NewCard(MDCard):
    """Dynamically generated News Card"""

    def __init__(self, title, description, source, time, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.md_bg_color = (0.1, 0.1, 0.1, 1)
        self.size_hint = (1, None)
        self.height = dp(120)
        self.elevation = 5
        self.spacing = dp(20)

        self.add_widget(MDLabel(text=source, font_style="Caption", font_size="15sp"))

        self.add_widget(
            MDLabel(
                text=title,
                font_style="H6",
                font_size="20sp",
                max_lines=2,
                adaptive_height=True,
            )
        )
        self.add_widget(
            MDLabel(text=description, font_style="H6", font_size="20sp", max_lines=2)
        )
        self.add_widget(MDLabel(text=time, font_style="Caption", font_size="15sp"))


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
                title=news["title"],
                description=news["description"],
                source=news["source"],
                time=news["time"],
            )
            news_grid.add_widget(news_card)
