from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from news_screen import NewsScreen
from home_screen import HomeScreen
from search_screen import SearchScreen
from favorite_screen import FavoriteManager
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

        self.root.ids.screen_manager.current = "home"
        # screen_manager = MDScreenManager()

        # screen_manager.add_widget(HomeScreen(name="home"))
        # screen_manager.add_widget(NewsScreen(name="news"))
        # screen_manager.add_widget(SearchScreen(name="search"))
        # screen_manager.add_widget(SearchScreen(name="search"))
        # screen_manager.add_widget(SearchScreen(name="search"))

        # screen_manager.current = "home"
        root = Builder.load_file("main.kv")

        return root

    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


if __name__ == "__main__":
    MainApp().run()
