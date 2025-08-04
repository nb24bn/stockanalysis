from data_loader import fetch_stock_data
from indicators import add_indicators
from strategy import generate_signal
from backtest import backtest_signals
from Visualize import plot_signals
from Score import score_stock


# Fetch data (Pass the ticker symbol like 'AAPL' for Apple)
df = fetch_stock_data('AAPL')

# Add technical indicators to the data
df = add_indicators(df)

# Generate trading signals based on the indicators
df = generate_signal(df)

# Print the latest 5 rows with relevant trading info
print(df[['Close', 'RSI', 'MACD', 'Signal_Line', 'Signal']].tail())

# Save output to CSV file
df.to_csv('signals_output.csv')

trades = backtest_signals(df)

plot_signals(df, title='AAPL - Signal Chart')

signal_score = score_stock(df)
print(f"📈 Final signal score for AAPL: {signal_score}/7")