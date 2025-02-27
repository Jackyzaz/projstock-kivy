from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


class Home_ScreenApp(MDApp):
    def build(self):
        return Builder.load_file("HomeScreen.kv")

    def on_start(self):
        stock_data = [
            (
                "Dow Jones",
                "$490.82",
                "$385.25",
                "$421.27",
                "-1.23",
                "2.4%",
                "43,428.02",
            ),
            ("S&P 500", "$225.87", "$124.87", "$171.48", "12.53", "5.8%", "6,013.13"),
            ("AAPL", "$1008.57", "$750.28", "$903.56", "7.56", "8.7%", "245.55"),
            ("BA", "$275.30", "$154.45", "$175.48", "-8.47", "8.8%", "177.15"),
            ("BRK-B", "$225.87", "$124.87", "$200.48", "0.98", "1.58%", "478.74"),
            ("DIS", "$1008.57", "$750.28", "$903.56", "7.56", "8.7%", "108.66"),
            ("S&P 500", "$225.87", "$124.87", "$171.48", "12.53", "5.8%", "6,013.13"),
            ("AAPL", "$1008.57", "$750.28", "$903.56", "7.56", "8.7%", "245.55"),
            ("BA", "$275.30", "$154.45", "$175.48", "-8.47", "8.8%", "177.15"),
            ("BRK-B", "$225.87", "$124.87", "$200.48", "0.98", "1.58%", "478.74"),
            ("DIS", "$1008.57", "$750.28", "$903.56", "7.56", "8.7%", "108.66"),
        ]
        stock_table = MDDataTable(
            background_color=(0.3, 0.3, 0.3, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1),
            column_data=[
                ("Company Name", dp(55)),
                ("High", dp(40)),
                ("Low", dp(40)),
                ("Prev Close", dp(40)),
                ("Change", dp(40)),
                ("Gain", dp(40)),
                ("5 Day Performance", dp(55)),
            ],
            row_data=[
                (
                    f"[b]{name}[/b]\n[i]{name} Inc.[/i]",
                    high,
                    low,
                    prev,
                    f"[color={self.get_color(change)}]{change}[/color]",
                    f"[color={self.get_color(gain)}]{gain}[/color]",
                    performance,
                )
                for name, high, low, prev, change, gain, performance in stock_data
            ],
            check=True,
        )

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        self.root.ids.stock_table_box.add_widget(stock_table)

    def get_color(self, value):
        try:
            return "00FF00" if float(value) > 0 else "FF0000"
        except:
            return "FFFFFF"


if __name__ == "__main__":
    Home_ScreenApp().run()
