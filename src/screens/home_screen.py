from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
import os

KV_FILE = os.path.join(os.path.dirname(__file__), "HomeScreen.kv")


class HomeScreen(Screen):
    pass


class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file(KV_FILE) or HomeScreen()


if __name__ == "__main__":
    TestApp().run()
