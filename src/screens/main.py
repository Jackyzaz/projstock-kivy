from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from news_screen import NewsScreen
from home_screen import HomeScreen



class MainApp(MDApp):
    def build(self):
        # กำหนดธีมของแอป
        self.theme_cls.primary_palette = "Blue"  # กำหนดสีหลักเป็นสีน้ำเงิน
        self.theme_cls.theme_style = "Dark"  # กำหนดธีมเป็น Dark Mode

        # สร้าง MDScreenManager
        screen_manager = MDScreenManager()

        # เพิ่มหน้าจอ NewsScreen และ HomeScreen
        screen_manager.add_widget(NewsScreen(name="news"))
        screen_manager.add_widget(HomeScreen(name="home"))

        # ตั้งค่าให้แสดงหน้าจอ "news" เป็นค่าเริ่มต้น
        screen_manager.current = "home"  

        return screen_manager

if __name__ == "__main__":
    MainApp().run()
