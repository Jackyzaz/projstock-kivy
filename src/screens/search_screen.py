from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton

class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        