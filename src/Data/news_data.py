import yfinance as yf
from datetime import datetime

def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news_list = stock.get_news()

    if not news_list:
        return []

    return news_list
    
news_data = fetch_stock_news("NVDA")
for x in news_data:
    print(x)
