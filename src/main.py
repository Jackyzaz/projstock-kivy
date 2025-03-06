from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from screens.home_screen import HomeScreen
from screens.news_screen import NewsScreen


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home_screen"))
        return sm


if __name__ == "__main__":
    MainApp().run()
