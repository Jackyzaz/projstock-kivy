import os
import csv


def fetch_stock_symbols():
    """
    อ่านสัญลักษณ์หุ้นจากไฟล์ CSV
    """
    stock_file = os.path.join(os.path.dirname(__file__), "../screens/stocks.csv")
    stock_list = []
    try:
        with open(stock_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    symbol, company = row[0], row[1]
                    stock_list.append(f"{symbol} ({company})")
        return stock_list
    except FileNotFoundError:
        print("stocks.csv not found, using default list")
        return []
    except Exception as e:
        print(f"Error reading stocks.csv: {e}")
        return []
