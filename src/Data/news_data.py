import yfinance as yf

def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news_list = stock.get_news()

    if not news_list:
        return []

    return news_list
    

news_data = fetch_stock_news("NVDA")

for news in news_data:
    print(news)
