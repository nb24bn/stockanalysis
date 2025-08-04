import pandas as pd
import datetime
import joblib
from data_loader import fetch_stock_data
from indicators import add_indicators
from strategy import generate_signal
from Score import score_stock
from news_fetcher import fetch_recent_news
from backtest import backtest_signals

# Load model once
model = joblib.load("stock_predictor.pkl")

# Load tickers
tickers_df = pd.read_csv("tickers.csv")
tickers = tickers_df['Ticker'].dropna().unique().tolist()

results = []

for ticker in tickers:
    print(f"🔍 Processing: {ticker}")
    try:
        df = fetch_stock_data(ticker, start='2015-01-01', end='2025-12-31', interval='1d')
        df = add_indicators(df)
        df = generate_signal(df)

        score, label = score_stock(df)
        signal = df['Signal'].iloc[-1]
        close = df['Close'].iloc[-1]
        news = fetch_recent_news(ticker)

        features = df[['RSI', 'SMA_20', 'SMA_50', 'MACD', 'Signal_Line', 'BB_High', 'BB_Low', 'ATR', 'Volume_Z']].tail(1).dropna()

        if not features.empty:
            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0]
            confidence = max(proba) * 100
            prediction_label = "High Potential" if prediction == 1 else "Not High Potential"
        else:
            prediction_label = "Insufficient Data"
            confidence = 0

        results.append({
            "Ticker": ticker,
            "Signal": signal,
            "Score": score,
            "Label": label,
            "Prediction": prediction_label,
            "Confidence": round(confidence, 2),
            "Close": round(close, 2),
            "News": news
        })

    except Exception as e:
        print(f"⚠️ Skipping {ticker} due to error: {e}")

# Save to reports
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
df_result = pd.DataFrame(results)
output_path = f"reports/screener_report_{timestamp}.csv"
df_result.to_csv(output_path, index=False)
print(f"\n✅ Batch screening complete. Report saved to: {output_path}")
