from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class StockChartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.layout = GridLayout(
            cols=1,
            rows=3,
            padding=[50, 20, 50, 20],
            spacing=20,
            size_hint=(1, 1),
        )

        self.chart_label = Label(
            text="[Mock] Stock Chart",
            font_size=58,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=300,
        )

        self.back_button = Button(
            text="Back",
            size_hint_y=None,
            height=70,
            background_color=(0, 0.6, 1, 1),
            font_size=24,
            on_press=self.go_back,
        )

        self.layout.add_widget(self.chart_label)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def go_back(self, instance):
        self.manager.current = "home"
