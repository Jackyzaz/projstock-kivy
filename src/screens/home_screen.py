from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from stock_chart_screen import StockChartScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(
            orientation="vertical", padding=[25, 10, 25, 10], spacing=5
        )

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.label = Label(
            text="Stock Dashboard",
            font_size=48,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
        )

        def centered_widget(widget):
            box = BoxLayout(
                orientation="horizontal", padding=[25, 10, 25, 10], spacing=5
            )
            box.add_widget(Widget(size_hint_x=1))
            box.add_widget(widget)
            box.add_widget(Widget(size_hint_x=1))
            return box

        self.ticker_input = TextInput(
            hint_text="Enter Stock Symbol (e.g. AAPL)",
            size_hint=(None, None),
            width=600,
            height=60,
            background_color=(1, 1, 1, 0.2),
            multiline=False,
            font_size=40,
        )

        self.time_period_spinner = Spinner(
            text="1d",
            values=["1d", "1wk", "1mo", "1y", "max"],
            size_hint=(None, None),
            width=600,
            height=60,
            background_color=(0.3, 0.3, 0.3, 1),
            font_size=40,
        )

        self.show_chart_button = Button(
            text="Show Chart",
            size_hint_y=None,
            height=80,
            background_color=(0, 0.6, 1, 1),
            font_size=45,
        )

        main_layout.add_widget(self.label)
        main_layout.add_widget(Widget(size_hint_y=1))
        main_layout.add_widget(centered_widget(self.ticker_input))
        main_layout.add_widget(centered_widget(self.time_period_spinner))
        main_layout.add_widget(Widget(size_hint_y=1))
        main_layout.add_widget(self.show_chart_button)
        main_layout.add_widget(Widget(size_hint_y=1))

        self.add_widget(main_layout)

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
