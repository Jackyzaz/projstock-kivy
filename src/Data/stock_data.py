import yfinance as yf
import pandas as pd
from datetime import datetime,timedelta


def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == '1wk': 
        start_date = end_date - timedelta(days=7) 
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval) 
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data

def process_data(data):
    if data.empty:
        print("⚠️ No data retrieved. Check ticker, internet connection, or rate limits.")
        return data

    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('Asia/Bangkok') 
    data.reset_index(inplace=True)  
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

data = fetch_stock_data("NVDA","1wk","1h")
data = process_data(data)
print(data)  