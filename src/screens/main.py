from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from home_screen import HomeScreen
from news_screen import NewsScreen


class MainApp(MDApp):
    def build(self):
        # โหลดไฟล์ .kv ของแต่ละหน้า
        Builder.load_file("screens/HomeScreen.kv")
        Builder.load_file("screens/NewsScreen.kv")

        sm = MDScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(NewsScreen(name="news"))
        return sm

    def switch_screen(self, screen_name):
        self.root.current = screen_name