from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.stock_chart_screen import StockChartScreen


class StockDashboardApp(App):
    def build(self):
        Builder.load_file("stock_dashboard.kv")
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(StockChartScreen(name="stock_chart"))
        return sm


if __name__ == "__main__":
    StockDashboardApp().run()
