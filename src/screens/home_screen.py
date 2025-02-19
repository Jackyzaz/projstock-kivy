from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class HomeScreen(Screen):

    def show_chart(self):
        ticker = self.ids.ticker_input.text
        time_period = self.ids.time_period_spinner.text
        print(f"Ticker : {ticker} \nTime period : {time_period}")
        stock_chart_screen = self.manager.get_screen("stock_chart")
        stock_chart_screen.ticker = ticker
        stock_chart_screen.time_period = time_period

        self.ids.time_period_spinner.text = "1d"
        self.ids.ticker_input.text = ""
        self.manager.current = "stock_chart"
