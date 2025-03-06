import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.Data.stock_data import get_multiple_data
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


class News_ScreenApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.layout = Builder.load_file("NewsScreen.kv")
        self.row_data = []
        return self.layout


News_ScreenApp().run()
