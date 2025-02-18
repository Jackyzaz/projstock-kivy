from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def show_chart(self):
        self.manager.current = "stock_chart"
