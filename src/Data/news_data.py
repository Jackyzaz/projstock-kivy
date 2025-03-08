import yfinance as yf
from datetime import datetime
import json


def fetch_stock_info(ticker):
    """Fetch stock details such as name, value, and market status."""
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    return {
        "stock_name": stock_info.get("symbol", "N/A"),
        "stock_fullname": stock_info.get("longName", "N/A"),
        "stock_value": stock_info.get("regularMarketPrice", "N/A"),
        "stock_change": stock_info.get("regularMarketChange", "N/A"),
        "stock_status": (
            "Market Open"
            if stock_info.get("marketState") == "REGULAR"
            else "Market Closed"
        ),
    }


def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news_list = stock.get_news()

    if not news_list:
        return []

    formatted_news = []

    for news in news_list:
        print(json.dumps(news, indent=2))
        content = news.get("content", {})
        thumbnail = content.get("thumbnail", {})
        provider = content.get("provider", {}).get("url", "Unknow Source")
        title = content.get("title", {})
        summary = content.get("summary", {})
        pubDate = content.get("pubDate", {})
        dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
        formatted_news.append(
            {
                "thumbnail": thumbnail,
                "provider": provider,
                "title": title,
                "summary": summary,
                "pubDate": dt_obj.strftime("%d/%m/%Y %H:%M:%S"),
            }
        )
    return formatted_news
