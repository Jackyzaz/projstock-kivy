import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from yfinance.exceptions import YFPricesMissingError


def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == "1wk":
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data


def process_timezone(data):
    if data.empty:
        print("⚠️ No data retrieved. Check ticker, internet connection, or rate limits.")
        return data

    if data.index.tzinfo is None:
        data.index = data.index.tz_localize("UTC")
    data.index = data.index.tz_convert("Asia/Bangkok")
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "Datetime"}, inplace=True)
    return data


def get_data(name, period, interval):
    data = fetch_stock_data(name, period, interval)
    data = process_timezone(data)
    return data


def get_multiple_data(tickers, period, interval):
    all_data = {}
    for ticker in tickers:
        try:
            data = get_data(ticker, period, interval)
            if not data.empty:
                all_data[ticker] = data
        except YFPricesMissingError:
            print(f"No data found for {ticker}. It may be delisted.")
    return all_data
