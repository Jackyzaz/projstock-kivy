import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.data.stock_data import get_multiple_data
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
import yfinance as yf
from datetime import datetime
from kivy.uix.scrollview import ScrollView
import pandas as pd


def fetch_stock_news(tickers=None):
    """ดึงข่าวจาก yfinance ของหลายหุ้น"""
    if tickers is None:
        tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "NVDA"]

    formatted_news = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            news_list = stock.get_news()
        except Exception:
            formatted_news.append(
                {
                    "ticker": ticker,
                    "title": "Failed to Load News",
                    "summary": "Please try again.",
                    "pubDate": "-",
                }
            )
            continue

        if not news_list:
            formatted_news.append(
                {
                    "ticker": ticker,
                    "title": "No News Available",
                    "summary": "No recent news found.",
                    "pubDate": "-",
                }
            )
            continue

        for news in news_list[:3]:
            content = news.get("content", {})
            title = content.get("title", "No Title")
            summary = content.get("summary", "No Summary")
            pubDate = content.get("pubDate", "-")

            try:
                dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
            except:
                formatted_date = "Unknown Date"

            formatted_news.append(
                {
                    "ticker": ticker,
                    "title": title,
                    "summary": summary,
                    "pubDate": formatted_date,
                }
            )

    return formatted_news


class News_ScreenApp(MDApp):
    pass


News_ScreenApp().run()
