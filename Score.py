import pandas as pd

def score_stock(df):
    df = df.copy()
    latest = df.iloc[-1]
    score = 0

    # --- Condition 1: RSI in buy zone (oversold)
    if pd.notna(latest['RSI']) and latest['RSI'] < 45:
        score += 1

    # --- Condition 2: SMA crossover (bullish)
    if pd.notna(latest['SMA_20']) and pd.notna(latest['SMA_50']) and latest['SMA_20'] > latest['SMA_50']:
        score += 1

    # --- Condition 3: MACD crossover bullish
    if len(df) >= 2 and pd.notna(df['MACD'].iloc[-2]) and pd.notna(df['Signal_Line'].iloc[-2]):
        if df['MACD'].iloc[-2] < df['Signal_Line'].iloc[-2] and latest['MACD'] > latest['Signal_Line']:
            score += 2

    # --- Condition 4: Price breakout (above Bollinger Band high)
    if pd.notna(latest['Close']) and pd.notna(latest['BB_High']) and latest['Close'] > latest['BB_High']:
        score += 1

    # --- Condition 5: Volume spike
    if pd.notna(latest['Volume_Z']) and latest['Volume_Z'] > 1:
        score += 1

    # --- Condition 6: Signal is BUY
    if 'Signal' in latest and latest['Signal'] == 'BUY':
        score += 2

    # --- Final label assignment
    label = "High Potential" if score >= 3 else "Not High Potential"  # previously: >=5

    return score, label
