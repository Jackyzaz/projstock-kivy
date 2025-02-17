import yfinance as yf

symbol = "ADVANC.BK"
stock = yf.Ticker(symbol)

df = stock.history(period="1d")
print(df)