from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from news_screen import NewsScreen
from home_screen import HomeScreen
from search_screen import SearchScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.tools.hotreload.app import MDApp
from kivy.core.window import Window

class MainApp(MDApp):
    # KV_FILES = ["./src/screens/SearchScreen.kv"]
    # DEBUG=True

    # Just build_app and delete first=False
    def build(self):
        Window.size = (1280, 720)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        screen_manager = MDScreenManager()

        screen_manager.add_widget(SearchScreen(name="search"))
        screen_manager.add_widget(NewsScreen(name="news"))
        screen_manager.add_widget(HomeScreen(name="home"))

        root = Builder.load_file("main.kv")

        screen_manager.current = "search"

        return root

    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


if __name__ == "__main__":
    MainApp().run()
