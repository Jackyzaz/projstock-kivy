import yfinance as yf
from datetime import datetime
import json


def fetch_stock_info(ticker):
    """Fetch stock details with error handling."""
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Handle case where stock.info is None
        if not stock_info or stock_info == {}:
            raise ValueError(f"No data found for ticker: {ticker}")

        return {
            "stock_name": stock_info.get("symbol", ticker.upper()),
            "stock_fullname": stock_info.get("longName", "Unknown Stock"),
            "stock_value": stock_info.get("regularMarketPrice", "N/A"),
            "stock_change": stock_info.get("regularMarketChange", "N/A"),
            "stock_status": (
                "Market Open"
                if stock_info.get("marketState") == "REGULAR"
                else "Market Closed"
            ),
        }

    except Exception as e:
        print(f"Error fetching stock info for {ticker}: {e}")

        # Return default/fallback stock info
        return {
            "stock_name": ticker.upper(),
            "stock_fullname": "(Stock Data Unavailable)",
            "stock_value": "N/A",
            "stock_change": "N/A",
            "stock_status": "Unavailable",
        }


def fetch_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news_list = stock.get_news()

    if not news_list:
        return []

    formatted_news = []

    for news in news_list:
        # print(json.dumps(news, indent=2)) # Use this line to logs
        content = news.get("content", {})
        provider = content.get("provider", {}).get("url", "Unknow Source")

        # Ensure 'clickThroughUrl' is an object (dict) before accessing 'url'
        click_through_obj = content.get("clickThroughUrl", {})
        click_through_url = (
            click_through_obj.get("url", "Unknown Source")
            if isinstance(click_through_obj, dict)
            else "Unknown Source"
        )

        title = content.get("title", {})
        summary = content.get("summary", {})
        pubDate = content.get("pubDate", {})
        dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
        formatted_news.append(
            {
                "provider": provider,
                "click_through_url": click_through_url,
                "title": title,
                "summary": summary,
                "pubDate": dt_obj.strftime("%d/%m/%Y %H:%M:%S"),
            }
        )
        print(json.dumps(formatted_news, indent=2))
    return formatted_news
