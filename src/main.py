from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens.home_screen import HomeScreen
from screens.stock_chart_screen import StockChartScreen

class MainApp(App):
    def build(self):
        Builder.load_file("screens/HomeScreen.kv")
        Builder.load_file("screens/StockChartScreen.kv")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(StockChartScreen(name="stock_chart"))

        return sm

if __name__ == "__main__":
    MainApp().run()
