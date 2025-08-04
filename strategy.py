def generate_signal(df):
    df['Signal'] = 'HOLD'  # Default signal

    for i in range(1, len(df)):
        # Fetch values
        rsi = df['RSI'].iloc[i]
        macd = df['MACD'].iloc[i]
        signal_line = df['Signal_Line'].iloc[i]
        sma_20 = df['SMA_20'].iloc[i]
        sma_50 = df['SMA_50'].iloc[i]

        # Debug print for inspection
        print(f"Date: {df.index[i]} | RSI: {rsi:.2f} | MACD: {macd:.2f} | Signal Line: {signal_line:.2f} | SMA_20: {sma_20:.2f} | SMA_50: {sma_50:.2f}")

        # Relaxed signal logic for testing
        if sma_20 > sma_50 and rsi < 50:
            df.at[df.index[i], 'Signal'] = 'BUY'
        elif sma_20 < sma_50 and rsi > 50:
            df.at[df.index[i], 'Signal'] = 'SELL'
        else:
            df.at[df.index[i], 'Signal'] = 'HOLD'

    return df
