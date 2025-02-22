import yfinance as yf
import pandas as pd
from datetime import datetime


def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    data = yf.download(ticker, period=period, interval=interval)
    return data

data = fetch_stock_data("NVDA","1d","30m")
print(data.head())  