from kivy.uix.label import Label
from kivy.app import App


class HomeScreen(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.label = Label(text="Stock Dashboard", font_size=24)
        return self.label


if __name__ == "__main__":
    HomeScreen().run()
