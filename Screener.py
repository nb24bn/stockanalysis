import pandas as pd
import joblib
import os

from data_loader import fetch_stock_data
from indicators import add_indicators
from strategy import generate_signal
from Score import score_stock
from news_fetcher import fetch_recent_news

def screen_stocks(ticker_list, use_ml=True):
    results = []

    # Load ML model if available and enabled
    model = None
    if use_ml and os.path.exists("stock_predictor.pkl"):
        model = joblib.load("stock_predictor.pkl")

    for ticker in ticker_list:
        try:
            print(f"\n🔍 Processing {ticker}...")
            df = fetch_stock_data(ticker, start='2020-01-01', end='2025-12-31', interval='1d')
            df = add_indicators(df)
            df = generate_signal(df)

            score, label = score_stock(df)
            signal = df['Signal'].iloc[-1]
            close = df['Close'].iloc[-1]
            news = fetch_recent_news(ticker)

            # ML prediction
            prediction_label = ""
            confidence = ""
            if model:
                features = df[[
                    'RSI', 'SMA_20', 'SMA_50', 'MACD', 'Signal_Line',
                    'BB_High', 'BB_Low', 'ATR', 'Volume_Z'
                ]].tail(1).dropna()

                if not features.empty:
                    pred = model.predict(features)[0]
                    prob = model.predict_proba(features)[0]
                    prediction_label = "High Potential" if pred == 1 else "Not High Potential"
                    confidence = round(max(prob) * 100, 2)

            results.append({
                'Ticker': ticker,
                'Close': round(close, 2),
                'Signal': signal,
                'Rule-Based Score': score,
                'Rule-Based Label': label,
                'ML Prediction': prediction_label,
                'Confidence (%)': confidence,
                'News': news
            })

        except Exception as e:
            print(f"⚠️ Skipping {ticker} due to error: {e}")

    # Sort and save
    result_df = pd.DataFrame(results).sort_values(by='Rule-Based Score', ascending=False)
    result_df.to_csv("top_stock_recommendations.csv", index=False)
    print("\n📊 Screener completed. Results saved to 'top_stock_recommendations.csv'.")
    print(result_df.head())

    return result_df

# 🔍 CLI usage or import from app.py
if __name__ == "__main__":
    try:
        tickers_df = pd.read_csv("tickers.csv")
        ticker_list = tickers_df['Ticker'].dropna().unique().tolist()
    except:
        ticker_list = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'TCS.NS', 'INFY.NS', 'RELIANCE.NS']

    screen_stocks(ticker_list)
