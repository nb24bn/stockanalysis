import pandas as pd
from data_loader import fetch_stock_data
from indicators import add_indicators
from strategy import generate_signal
from Score import score_stock

# ✅ List of tickers to process
tickers = ['AAPL', 'TSLA', 'INFY.NS', 'RELIANCE.NS', '^NSEI', 'VOO']

# ✅ Storage for all processed rows
final_data = []

for ticker in tickers:
    print(f"🔄 Processing: {ticker}")
    try:
        df = fetch_stock_data(ticker, start='2015-01-01', end='2025-12-31', interval='1d')
        df = add_indicators(df)
        df = generate_signal(df)

        # Add Ticker
        df['Ticker'] = ticker

        # --- Scoring and Labeling each row (for ML training) ---
        scores = []
        labels = []

        for i in range(len(df)):
            try:
                temp_df = df.iloc[:i+1].copy()
                s, l = score_stock(temp_df)
                scores.append(s)
                labels.append(l)
            except Exception as e:
                scores.append(None)
                labels.append(None)

        df['Score'] = scores
        df['Label'] = labels

        # Select required columns & clean
        selected = df[[
            'Ticker', 'Close', 'RSI', 'SMA_20', 'SMA_50',
            'MACD', 'Signal_Line', 'BB_High', 'BB_Low',
            'ATR', 'Volume_Z', 'Label'
        ]].dropna()

        final_data.append(selected)

    except Exception as e:
        print(f"❌ Error processing {ticker}: {e}")

# ✅ Concatenate and export
if final_data:
    full_df = pd.concat(final_data, ignore_index=True)
    full_df.to_csv("training_data.csv", index=False)
    print(f"✅ Saved enriched training data to training_data.csv ({len(full_df)} rows)")
else:
    print("⚠️ No data was generated. Check tickers or data pipeline.")
