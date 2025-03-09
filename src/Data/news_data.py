import yfinance as yf
from datetime import datetime
import concurrent.futures
import asyncio
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


async def fetch_stock_news_async(ticker):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        news = await loop.run_in_executor(executor, fetch_stock_news_worker, ticker)
    return news


def fetch_stock_news_worker(ticker):
    try:
        stock = yf.Ticker(ticker)
        news_list = stock.get_news()

        if not news_list:
            return []

        formatted_news = []
        for news in news_list:
            # print(json.dumps(news, indent=2)) # for log
            content = news.get("content", {})
            # Get nested value from obj
            click_through_obj = content.get("clickThroughUrl", {})
            click_through_url = click_through_obj.get("url", "unknow")

            provider = content.get("provider", {}).get("url", "Unknown Source")
            title = content.get("title", "No Title")
            summary = content.get("summary", "No Summary")
            pubDate = content.get("pubDate", "1970-01-01T00:00:00Z")

            try:
                dt_obj = datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
                pubDate_formatted = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
            except:
                pubDate_formatted = "Unknown Date"

            formatted_news.append(
                {
                    "click_through_url": click_through_url,
                    "provider": provider,
                    "title": title,
                    "summary": summary,
                    "pubDate": pubDate_formatted,
                }
            )
        return formatted_news

    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []


def fetch_stock_news(ticker):
    return asyncio.run(fetch_stock_news_async(ticker))
