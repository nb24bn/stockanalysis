import matplotlib
matplotlib.use('Agg')  # For Streamlit or server usage

import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_signals(df, title='Stock Signals', file_path='signal_chart.png', fib_levels=None):
    try:
        plt.figure(figsize=(14, 7))

        # --- Closing Price ---
        plt.plot(df['Close'], label='Close Price', color='black', linewidth=1)

        # --- Moving Averages ---
        if 'SMA_20' in df.columns:
            plt.plot(df['SMA_20'], label='SMA 20', linestyle='--', color='blue')
        if 'SMA_50' in df.columns:
            plt.plot(df['SMA_50'], label='SMA 50', linestyle='--', color='orange')
        if 'EMA_20' in df.columns:
            plt.plot(df['EMA_20'], label='EMA 20', linestyle=':', color='green')
        if 'EMA_50' in df.columns:
            plt.plot(df['EMA_50'], label='EMA 50', linestyle=':', color='purple')

        # --- Bollinger Bands ---
        if 'BB_High' in df.columns and 'BB_Low' in df.columns:
            plt.fill_between(df.index, df['BB_Low'], df['BB_High'], color='grey', alpha=0.2, label='Bollinger Bands')

        # --- BUY/SELL Signals ---
        if 'Signal' in df.columns:
            buy_signals = df[df['Signal'] == 'BUY']
            plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='BUY', s=60)

            sell_signals = df[df['Signal'] == 'SELL']
            plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='SELL', s=60)

        # --- Fibonacci Retracement Lines (Optional) ---
        if fib_levels:
            for label, level in fib_levels.items():
                plt.axhline(y=level, linestyle='dotted', alpha=0.7, label=f'Fib {label}')

        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(file_path)
        print(f"✅ Chart saved as '{file_path}'")

    except Exception as e:
        print(f"❌ Error generating chart: {e}")


def plotly_signals(df, title='Stock Signals'):
    fig = go.Figure()

    # --- Price Line ---
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='black')))

    # --- Moving Averages ---
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20', line=dict(dash='dot', color='blue')))
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50', line=dict(dash='dot', color='orange')))
    if 'EMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], mode='lines', name='EMA 20', line=dict(dash='dash', color='green')))
    if 'EMA_50' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], mode='lines', name='EMA 50', line=dict(dash='dash', color='purple')))

    # --- Bollinger Bands ---
    if 'BB_High' in df.columns and 'BB_Low' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_High'], mode='lines', name='BB High', line=dict(color='gray'), opacity=0.4))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Low'], mode='lines', name='BB Low', line=dict(color='gray'), opacity=0.4, fill='tonexty', fillcolor='rgba(128,128,128,0.1)'))

    # --- Signals ---
    if 'Signal' in df.columns:
        buy = df[df['Signal'] == 'BUY']
        sell = df[df['Signal'] == 'SELL']

        fig.add_trace(go.Scatter(
            x=buy.index, y=buy['Close'], mode='markers', name='BUY',
            marker=dict(symbol='triangle-up', color='green', size=10)
        ))
        fig.add_trace(go.Scatter(
            x=sell.index, y=sell['Close'], mode='markers', name='SELL',
            marker=dict(symbol='triangle-down', color='red', size=10)
        ))

    fig.update_layout(
        title=title,
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Price',
        autosize=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
