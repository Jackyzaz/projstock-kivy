import yfinance as yf
from datetime import datetime

def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news_list = stock.get_news()

    if not news_list:
        return []
    
    formatted_news = []

    for news in news_list:
        content = news.get("content", {})
        thumbnail = content.get("thumbnail", {})
        title = content.get("title", {})
        summary = content.get("summary", {})
        pubDate = content.get("pubDate",{})
        dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
        
        formatted_news.append({
        "thumbnail": thumbnail,
        "title": title,
        "summary": summary,
        "pubDate": dt_obj.strftime("%d/%m/%Y %H:%M:%S")
        })

    return formatted_news
    
news_data = fetch_stock_news("NVDA")
for x in news_data:
    print(x)
