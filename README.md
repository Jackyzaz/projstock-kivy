# Stock App
Application for viewing stocks, stock news, stock graphs, developed with KivyMD and connect with yfinance API.

## Contributor
[@Worachat-Songmuangnu](https://github.com/Worachat-Songmuangnu) - Worachat Songmuangnu 6710110370 <br>
[@Pyneola](https://github.com/Pyneola) - Weera Arsasutcharit 6710110393 <br>
[@Jackyzaz](https://github.com/Jackyzaz) - Soravit Sukkarn 6710110428 <br>

## Feature Overview

### **1. View Stock Overview**
  
The Stock Home Page is the central hub for tracking stock market updates and financial news. It provides real-time information about stock prices, market trends, and relevant news articles.

![Screen Recording 2025-03-09 220312](https://github.com/user-attachments/assets/72c8d10c-1438-45ea-b857-9de0cfd9fa51)

**2. Discovery News**

The News section in the stock tracking application provides real-time updates on financial news related to specific stocks. Users can access market insights, trends, and breaking news that may impact stock prices.

![Screen Recording 2025-03-09 223855](https://github.com/user-attachments/assets/38110948-4287-45f9-a0c2-21d3968f6851)

**3. Stock Graph Insight**

The Stock Chart Page provides users with a visual representation of stock price trends over different time periods. It helps users analyze stock performance and market fluctuations for informed decision-making.

![Screen Recording 2025-03-09 224550](https://github.com/user-attachments/assets/f46eda18-0f00-4e18-af21-4d019a2ca828)


**4. Favorite Stock**

The Favorite Stocks Page allows users to track and manage a personalized list of stocks. This feature helps users monitor their preferred stocks without searching for them repeatedly.

![Screen Recording 2025-03-09 225027](https://github.com/user-attachments/assets/9ec8da9f-b68b-49ff-ac84-0bf6eda815e7)

## Application Materials
### Widgets (47 totals)
```
main.kv (11)
  MDBoxLayout x1
  | MDNavigationRail x1
  |   |-MDNavigationRailFabButton x1
  |   |-MDNavigationRailItem x4
  |-MDScreenManager x1
      |-HomeScreen x1
      |-SearchScreen x1
      |-NewsScreen x1
      |-FavoriteScreen x1
```
```
HomeScreen.kv (9)
  HomeScreen
    |-MDBoxLayout x1
      |-MDBoxLayout x1
      |  |-MDBoxLayout x3  
      |  |-MDLabel x2
      |  |-MDRaisedButton x1
      |-ScrollView X1
```
```
NewsScreen.kv (24)
  <NewsScreen>
    |-MDBoxLayout x1
      |-MDBoxLayout x1
        |-MDBoxLayout x1
        |  |-MDBoxLayout x1
        |  | |-MDLabel x2 # Stock Info Section
        |  |-MDBoxLayout x1
        |    |-MDTextField x1
        |-MDBoxLayout x1
        |-MDBoxLayout x1
        |-MDBoxLayout x1
          |-MDScrollView x1
          |-MDGridLayout x1 # News Section
  <StockInfo>
    |-MDBoxLayout x1
    |  |-MDLabel x2
    |-MDBoxLayout x1
    |  |-MDLabel x2
    |-MDLabel x1

  <NewCard>
    |-MDLabel x4
```
```
SearchScreen.kv (3)
  <SearchScreen>
    |-MDTextField x1
    |-MDRaisedButton x1
    |-Widget x1 # Plot Graph Section

```
### Callbacks (31 totals)
####    KV Files (9 totals)
```
 kv/
  ├── main.kv (4)
  │     ├── MDNavigationRailFabButton - on_release: app.switch_screen("home")
  │     ├── MDNavigationRailItem (x3) - on_release: app.switch_screen("news" | "search" | "favorite")
  │
  ├── HomeScreen.kv (1)
  │     ├── MDRaisedButton - on_release: root.refresh_data()
  │
  ├── NewsScreen.kv (3)
  │     ├── <NewCard> - on_release: root.Push()
  │     ├── <NewsScreen> - MDTextField (on_text: root.auto_complete(self, self.text))
  │     │                ├── MDTextField (on_text_validate: root.get_stock_data(self.text.upper()))
  │
  ├── SearchScreen.kv (1)
  │     ├── <SearchScreen> - MDRaisedButton (on_press: root.fetch_data(self))
```

####     Python Files (22 totals)
```
 src/
  ├── main.py (1)
  │     ├── switch_screen(self, screen_name) - Called by navigation buttons
  │
  ├── home_screen.py (5)
  │     ├── Clock.schedule_interval(self.update_datetime, 1) - Update timestamp every second
  │     ├── Clock.schedule_once(self.load_data, 0) - Load data on screen enter
  │     ├── Clock.schedule_once(self.fetch_stock_data, 0.2) - Fetch stock data after delay
  │     ├── Clock.schedule_once(self.fetch_news_data, 0.2) - Fetch news after delay
  │
  ├── favorite_screen.py (3)
  │     ├── MDTextField - self.search_input.bind(text=self.on_text)
  │     ├── MDRaisedButton - on_release: self.add_stock
  │     ├── IconLeftWidget - on_release: lambda x, s=stock_code: self.remove_favorite(s)
  │
  ├── news_screen.py (3)
  │     ├── Clock.schedule_once(self.get_stock_info, 1) - Load stock info on startup
  │     ├── Clock.schedule_once(self.populate_news, dt) - Populate news dynamically
  │     ├── MDTextField - on_text: root.auto_complete(self, self.text)
  │
  ├── search_screen.py (5)
  │     ├── MDTextField - self.search_input.bind(text=..., on_focus=self.on_focus)
  │     ├── MDRectangleFlatButton - on_press=lambda instance, p=period: self.update_period(p)
  │     ├── Window.bind(on_touch_down=...) - Detect external clicks to close dropdown
  │     ├── Window.bind(on_key_down=...) - Handle keyboard navigation for suggestions
  │     ├── MDRaisedButton - on_press=lambda x: self.dialog.dismiss()
  │
  ├── stock_utils.py (3)
  │     ├── OneLineListItem - on_press=lambda x, s=stock_item: select_suggestion(...)
  │     ├── Window.bind(on_touch_down=...) - Close suggestion dropdown on external click
  │     ├── Window.bind(on_key_down=...) - Handle keyboard interaction in dropdown
  │
  ├── data/
  │     news_data.py (1)
  │       ├── fetch_stock_news_async(ticker) - Used in async execution (ThreadPoolExecutor)
  │     stock_data.py (1)
  │       ├── get_multiple_data_async(tickers, period, interval) - Used in async execution (ThreadPoolExecutor)

```



## For Developer
### Start

```sh
python -m venv venv
```

### Window

```sh
venv\Scripts\activate
```

### Mac / Linux

```sh
source venv/bin/activate
```

### Install requirement

```sh
pip install -r requirements.txt
```

### Start App
```sh
python src/screens/main.py
```
