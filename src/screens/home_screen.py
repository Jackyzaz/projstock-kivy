from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from stock_chart_screen import StockChartScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.ticker_input = TextInput(
            hint_text="Enter Stock Symbol (e.g. AAPL)",
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 0.2),  # gray color
            multiline=False,
        )

        self.time_period_spinner = Spinner(
            text="1d",
            values=["1d", "1wk", "1mo", "1y", "max"],
            background_color=(0.3, 0.3, 0.3, 1),  # black color
            size_hint_y=None,
            height=40,
        )

        self.show_chart_button = Button(
            text="Show Chart",
            size_hint_y=None,
            height=50,
            background_color=(0, 0.6, 1, 1),  # blue color
        )

        self.label = Label(text="Stock Dashboard", font_size=28, color=(1, 1, 1, 1))

        layout.add_widget(self.label)
        layout.add_widget(self.ticker_input)
        layout.add_widget(self.time_period_spinner)
        layout.add_widget(self.show_chart_button)
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class StockDashboardApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        # sm.add_widget(StockChartScreen(name="stock_chart"))  # Mock
        return sm


if __name__ == "__main__":
    StockDashboardApp().run()
