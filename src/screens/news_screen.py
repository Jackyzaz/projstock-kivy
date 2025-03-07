import sys
import os
import random
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from datetime import datetime, timedelta

# Sample news headlines
MOCK_NEWS_DATA = [
    {
        "title": "Stock Market Hits New High",
        "source": "finance.com",
        "time": "2 hours ago",
    },
    {
        "title": "Tech Giants Report Record Profits",
        "source": "businessnews.com",
        "time": "5 hours ago",
    },
    {
        "title": "Oil Prices Surge Amid Global Tensions",
        "source": "energywatch.com",
        "time": "8 hours ago",
    },
    {
        "title": "Cryptocurrency Market Sees Volatility",
        "source": "cryptoalert.com",
        "time": "1 day ago",
    },
    {
        "title": "Federal Reserve Announces Rate Changes",
        "source": "economytoday.com",
        "time": "12 hours ago",
    },
    {
        "title": "New Breakthrough in AI Technology",
        "source": "techreview.com",
        "time": "4 hours ago",
    },
]


class NewCard(MDCard):
    """Dynamically generated News Card"""

    def __init__(self, title, source, time, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.md_bg_color = (0.1, 0.1, 0.1, 1)
        self.size_hint = (1, None)
        self.height = dp(120)
        self.padding = dp(10)
        self.radius = [10, 10, 10, 10]
        self.elevation = 5

        self.add_widget(
            MDLabel(
                text=source, font_style="Caption", font_size="15sp", adaptive_size=True
            )
        )

        self.add_widget(
            MDLabel(
                text=title,
                font_style="H6",
                font_size="20sp",
                halign="left",
                valign="top",
                adaptive_height=True,
                max_lines=2,
            )
        )

        self.add_widget(
            MDLabel(
                text=time,
                font_style="Caption",
                font_size="15sp",
                halign="left",
                valign="top",
                adaptive_size=True,
            )
        )


class NewsScreen(MDScreen):
    """News Screen that dynamically populates news data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("NewsScreen.kv")  # Load the KV file

        # Get reference to the GridLayout in KV file
        # Ensure `id: news_grid` exists in .kv file

        # Generate and add mock news cards dynamically
        for news in MOCK_NEWS_DATA:
            news_card = NewCard(
                title=news["title"], source=news["source"], time=news["time"]
            )
            self.ids.news_grid.add_widget(news_card)

    def on_button_click(self):
        print("Button clicked in News Screen!")
