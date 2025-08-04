import pandas as pd
import yfinance as yf

def load_tickers_from_file(filepath="tickers.csv"):
    return pd.read_csv(filepath)

def fetch_stock_data(ticker: str, start='2015-01-01', end='2024-12-31', interval='1d'):
    data = yf.download(ticker, start=start, end=end, interval=interval)
    data.dropna(inplace=True)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data
