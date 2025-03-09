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

# App API Design
This app also leverages `yfinance`, `asyncio`, and `concurrent.futures` to optimize data fetching and ensure efficient handling of multiple requests, improving the app's performance and responsiveness.

### Home Screen

#### 1. `load_data()`
**Purpose**: Loads stock and news data when the Home Screen is entered.
```python
load_data()
```

#### 2. `fetch_stock_data()`
**Purpose**: Fetches stock data for the favorite stocks.
```python
fetch_stock_data()
```

#### 3. `fetch_news_data()`
**Purpose**: Fetches the latest news for the first favorite stock (or NVDA if no favorites).
```python
fetch_news_data()
```

### News Screen

#### 1. `get_stock_data(stock_id)`
**Purpose**: Fetches stock data and news for a specific stock ID and updates the stock info and news grid on the screen.
```python
get_stock_data("AAPL")
```

#### 2. `get_stock_info(dt=None)`
**Purpose**: Loads stock information for the default favorite stock or NVDA and updates the stock info and news grid.
```python
get_stock_info()
```

#### 3. `Push()`
**Purpose**: Opens a web link for the news item in a browser when a news card is clicked.
```python
Push()
```

### Search Screen

#### 1. `plot_stock_data(symbol, period)`
**Purpose**: Fetches and plots the stock data for the specified symbol and time period.
```python
plot_stock_data("AAPL", "1d")
```

#### 2. `fetch_stock_symbols()`
**Purpose**: Fetches a list of all available stock symbols from a CSV file for use in the auto-completion feature.
```python
stock_symbols = fetch_stock_symbols()
```

#### 3. `auto_complete(instance, value)`
**Purpose**: Handles auto-suggestions for stock symbols or company names based on user input in the search bar.
```python
auto_complete(instance, "example text")
```

## Optimizing Performance with `yfinance`, `asyncio`, and `concurrent.futures`

### **yfinance**
`yfinance` is used to fetch stock data efficiently by retrieving historical market data, such as stock prices, volumes, and other financial metrics. It is integrated with the app to pull data for various stock symbols, with asynchronous fetching implemented to allow multiple stock requests to be handled in parallel.

### **Asyncio and Concurrent Futures**
To enhance performance when making multiple stock or news data requests, the app uses Python’s **`asyncio`** and **`concurrent.futures`** modules. 

- **`asyncio`** allows the app to execute asynchronous tasks, enabling non-blocking operations when fetching stock data and news.
- **`concurrent.futures`** is used to execute functions in parallel, allowing multiple data fetch requests (e.g., fetching data for multiple stocks or news sources) to run concurrently, reducing waiting time and improving response time for the user.

### Example Usage with `asyncio` and `concurrent.futures`

```python
import asyncio
import concurrent.futures
import yfinance as yf

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="1d")

async def fetch_multiple_stocks(stock_symbols):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(executor, fetch_stock_data, symbol)
            for symbol in stock_symbols
        ]
        results = await asyncio.gather(*tasks)
    return results

# Fetch data for multiple stocks concurrently
stock_symbols = ["AAPL", "GOOG", "AMZN"]
data = asyncio.run(fetch_multiple_stocks(stock_symbols))
```

### Benefits:
- **Non-blocking operations**: `asyncio` allows the app to continue running other operations while waiting for data to be fetched, providing a smoother user experience.
- **Parallel requests**: `concurrent.futures` optimizes fetching multiple stock data or news at once, reducing the overall time it takes to fetch data.


## Application Materials
### Widgets (58 totals)
```
main.kv (11)
├── MDBoxLayout (x1)
│   ├── MDNavigationRail (x1)
│   │   ├── MDNavigationRailFabButton (x1)
│   │   ├── MDNavigationRailItem (x4)
│   ├── MDScreenManager (x1)
│       ├── HomeScreen (x1)
│       ├── SearchScreen (x1)
│       ├── NewsScreen (x1)
│       ├── FavoriteScreen (x1)

HomeScreen.kv (9)
├── HomeScreen
│   ├── MDBoxLayout (x1)
│   │   ├── MDBoxLayout (x1)
│   │   │   ├── MDBoxLayout (x3)
│   │   │   ├── MDLabel (x2)
│   │   │   ├── MDRaisedButton (x1)
│   │   ├── ScrollView (x1)

NewsScreen.kv (24)
├── <NewsScreen>
│   ├── MDBoxLayout (x1)
│   │   ├── MDBoxLayout (x1)
│   │   │   ├── MDBoxLayout (x1)
│   │   │   │   ├── MDBoxLayout (x1)
│   │   │   │   │   ├── MDLabel (x2) # Stock Info Section
│   │   │   │   ├── MDBoxLayout (x1)
│   │   │   │   │   ├── MDTextField (x1)
│   │   │   ├── MDBoxLayout (x1)
│   │   │   ├── MDBoxLayout (x1)
│   │   │   ├── MDBoxLayout (x1)
│   │   │   │   ├── MDScrollView (x1)
│   │   │   │   ├── MDGridLayout (x1) # News Section
│
├── <StockInfo>
│   ├── MDBoxLayout (x1)
│   │   ├── MDLabel (x2)
│   ├── MDBoxLayout (x1)
│   │   ├── MDLabel (x2)
│   ├── MDLabel (x1)
│
├── <NewCard>
│   ├── MDLabel (x4)

SearchScreen.kv (3)
├── <SearchScreen>
│   ├── MDTextField (x1)
│   ├── MDRaisedButton (x1)
│   ├── Widget (x1) # Plot Graph Section

search_screen.py (6)
├── layout <BoxLayout> x1
|   ├── search_input <MDTextField> x1
|   ├── suggestion_list <MDList> x1
|   ├── period_layout <BoxLayout> x1
|   |   ├── btn <MDRectangleFlatButton> x1
|   ├──chart <FigureCanvasKivyAgg> x1

favorite_screen.py (5)
├── layout <BoxLayout> x1
|   ├── search_input <MDTextField> x1
|   ├── search_button <MDRaisedButton> x1
|   ├── scroll_view <MDScrollView> x1 
|       ├── favorite_list <MDList> x1
```
### Callbacks (22 totals)
```
  src/
  ├── screens/
  │     ├── main.py (1)
  │     │     ├── switch_screen(self, screen_name) - Called by navigation buttons
  │     ├── home_screen.py (5)
  │     │     ├── Clock.schedule_interval(self.update_datetime, 1) - Update timestamp every second
  │     │     ├── Clock.schedule_once(self.load_data, 0) - Load data on screen enter
  │     │     ├── Clock.schedule_once(self.fetch_stock_data, 0.2) - Fetch stock data after delay
  │     │     ├── Clock.schedule_once(self.fetch_news_data, 0.2) - Fetch news after delay
  │     │
  │     ├── favorite_screen.py (3)
  │     │     ├── MDTextField - self.search_input.bind(text=self.on_text)
  │     │     ├── MDRaisedButton - on_release: self.add_stock
  │     │     ├── IconLeftWidget - on_release: lambda x, s=stock_code: self.remove_favorite(s)
  │     │
  │     ├── news_screen.py (3)
  │     │     ├── Clock.schedule_once(self.get_stock_info, 1) - Load stock info on startup
  │     │     ├── Clock.schedule_once(self.populate_news, dt) - Populate news dynamically
  │     │     ├── MDTextField - on_text: root.auto_complete(self, self.text)
  │     │
  │     ├── search_screen.py (5)
  │     │     ├── MDTextField - self.search_input.bind(text=..., on_focus=self.on_focus)
  │     │     ├── MDRectangleFlatButton - on_press=lambda instance, p=period: self.update_period(p)
  │     │     ├── Window.bind(on_touch_down=...) - Detect external clicks to close dropdown
  │     │     ├── Window.bind(on_key_down=...) - Handle keyboard navigation for suggestions
  │     │     ├── MDRaisedButton - on_press=lambda x: self.dialog.dismiss()
  │     │
  │     ├── stock_utils.py (3)
  │     │     ├── OneLineListItem - on_press=lambda x, s=stock_item: select_suggestion(...)
  │     │     ├── Window.bind(on_touch_down=...) - Close suggestion dropdown on external click
  │     │     ├── Window.bind(on_key_down=...) - Handle keyboard interaction in dropdown
  │
  ├── data/
  │     ├── news_data.py (1)
  │     │     ├── fetch_stock_news_async(ticker) - Used in async execution (ThreadPoolExecutor)
  │     ├── stock_data.py (1)
  │     │     ├── get_multiple_data_async(tickers, period, interval) - Used in async execution (ThreadPoolExecutor)
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
