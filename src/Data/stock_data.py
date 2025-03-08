import yfinance as yf
import pandas as pd
import numpy as np
from scipy.interpolate import splrep, splev
import mplcyberpunk
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from yfinance.exceptions import YFPricesMissingError
import concurrent.futures
import requests
import asyncio


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


def fetch_single_stock(ticker, session, period, interval):
    try:
        stock = yf.Ticker(ticker, session=session)
        data = stock.history(period=period, interval=interval)
        if not data.empty:
            return ticker, process_timezone(data)
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
    return ticker, None


async def get_multiple_data_async(tickers, period, interval):
    all_data = {}
    session = requests.Session()  # ใช้ session เดียว ลดการสร้าง connection ใหม่

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=6
    ) as executor:  # ลด Worker เพื่อไม่ให้ CPU ใช้หนักเกิน
        futures = [
            loop.run_in_executor(
                executor, fetch_single_stock, ticker, session, period, interval
            )
            for ticker in tickers
        ]

        results = await asyncio.gather(*futures)
        for ticker, data in results:
            if data is not None:
                all_data[ticker] = data

    return all_data


def get_multiple_data(tickers, period, interval):
    return asyncio.run(get_multiple_data_async(tickers, period, interval))


def plot_stock_data(ticker, period, interval):
    data = get_data(ticker, period, interval)
    if data.empty:
        print(f"⚠️ No data retrieved for {ticker}.")
        return

    # Calculate smoothed close prices
    data["Close_smooth"] = data["Close"].rolling(window=7, min_periods=1).mean()
    if data["Close_smooth"].iloc[-1] < data["Close_smooth"].iloc[0]:
        overall_color = "#FF4C4C"
    else:
        overall_color = "#4CFF4C"

    # Spline interpolation for smoother line
    spl_close = splrep(
        data["Datetime"].astype(int) / 10**9, data["Close_smooth"], s=len(data) * 0.01
    )

    plt.style.use("dark_background")
    plt.figure(figsize=(10, 6))

    plt.plot(
        data["Datetime"],
        splev(data["Datetime"].astype(int) / 10**9, spl_close),
        label=f"{ticker} Price",
        linewidth=1.5,
        color=overall_color,
    )

    mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)
    plt.box(False)
    plt.grid(
        True,
        which="both",
        axis="both",
        color="gray",
        linestyle="-",
        linewidth=0.5,
        alpha=0.2,
    )
    plt.xticks(color="white")
    plt.yticks(color="white")

    return plt
