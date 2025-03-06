import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.Data.stock_data import get_multiple_data
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
import yfinance as yf
from datetime import datetime
from kivy.uix.scrollview import ScrollView
import pandas as pd
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineListItem

class NewsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    
#test click
    def on_button_click(self):
        print("Button clicked in News Screen!")


