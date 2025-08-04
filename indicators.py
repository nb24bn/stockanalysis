import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, SMAIndicator, MACD
from ta.volatility import BollingerBands, AverageTrueRange

def add_indicators(df):
    df = df.copy()

    # --- Ensure required columns exist ---
    required = ['Close', 'High', 'Low', 'Volume']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # --- RSI ---
    df['RSI'] = RSIIndicator(close=df['Close']).rsi()

    # --- Moving Averages ---
    df['SMA_20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
    df['SMA_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['EMA_20'] = EMAIndicator(close=df['Close'], window=20).ema_indicator()
    df['EMA_50'] = EMAIndicator(close=df['Close'], window=50).ema_indicator()

    # --- MACD & Signal Line ---
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['Signal_Line'] = macd.macd_signal()

    # --- Bollinger Bands ---
    bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()

    # --- ATR (Average True Range) ---
    atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14)
    df['ATR'] = atr.average_true_range()

    # --- Volume Metrics ---
    df['Volume_SMA_20'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Z'] = (df['Volume'] - df['Volume_SMA_20']) / df['Volume'].rolling(window=20).std()

    # --- On-Balance Volume (OBV) ---
    df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()

    return df


# --- Optional: Fibonacci Retracement Helper (not merged into df directly) ---
def fibonacci_levels(df):
    """
    Returns a dictionary of key Fibonacci retracement levels based on recent swing high/low.
    You can visualize this separately in Plotly.
    """
    recent_high = df['High'].iloc[-30:].max()
    recent_low = df['Low'].iloc[-30:].min()
    diff = recent_high - recent_low

    levels = {
        '0.0%': recent_high,
        '23.6%': recent_high - 0.236 * diff,
        '38.2%': recent_high - 0.382 * diff,
        '50.0%': recent_high - 0.5 * diff,
        '61.8%': recent_high - 0.618 * diff,
        '78.6%': recent_high - 0.786 * diff,
        '100.0%': recent_low
    }
    return levels
