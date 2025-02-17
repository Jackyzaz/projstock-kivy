import yfinance as yf
import pandas as pd

class StockData:
    def __init__(self,stock_symbol):
        self.stock_symbol = stock_symbol
    def fetch_stock_data(self):
        stock = yf.Ticker(self.stock_symbol)
        data = stock.history(period="6mo")
        return data

    def get_stock_info(self):
        stock = yf.Ticker(self.stock_symbol)
        return stock.info

stock = StockData("NVDA")
all_info= stock.get_stock_info()
print("Stock Name: ",all_info["displayName"])
print("Current Price:",all_info["currentPrice"],"USD" )
