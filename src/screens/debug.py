from kivy.lang import Builder
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from news_screen import NewsScreen
from home_screen import HomeScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window

# Builder.load_file("NewsScreen.kv")
# Builder.load_file("HomeScreen.kv")
Window.size = (1280, 720)


class DebugApp(MDApp):
    KV_FILES = ["./src/screens/NewsScreen.kv"]
    DEBUG = True

    def build_app(self, first=False):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        screen_manager = MDScreenManager()

        screen_manager.add_widget(NewsScreen(name="news"))
        # screen_manager.add_widget(HomeScreen(name="home"))

        root = Builder.load_file("debug.kv")

        screen_manager.current = "news"

        return root

    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


if __name__ == "__main__":
    DebugApp().run()
