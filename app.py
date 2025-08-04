import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
import joblib

from data_loader import fetch_stock_data
from indicators import add_indicators, fibonacci_levels
from strategy import generate_signal
from Score import score_stock
from news_fetcher import fetch_recent_news
from Screener import screen_stocks
from db import insert_signal_data, fetch_signal_history
from backtest import backtest_signals
from Visualize import plot_signals, plotly_signals

# Load model
@st.cache_resource
def load_model():
    return joblib.load("stock_predictor.pkl")

model = load_model()

@st.cache_data(show_spinner=False, ttl=3600)
def load_stock_data(ticker, start, end, interval):
    return fetch_stock_data(ticker, start, end, interval)

@st.cache_data(show_spinner=False)
def process_indicators(df):
    df = add_indicators(df)
    return generate_signal(df)

# Streamlit page config
st.set_page_config("📈 SmartStock Screener", layout="wide")
st.markdown("<h1 style='color:#1a73e8;'>📈 SmartStock: AI-Powered Signal Screener</h1>", unsafe_allow_html=True)

# Ticker input
try:
    tickers_df = pd.read_csv("tickers.csv")
    ticker_options = tickers_df['Ticker'].dropna().unique().tolist()
except:
    ticker_options = ['AAPL', 'TSLA', 'VOO', '^NSEI', 'INFY.NS', 'RELIANCE.NS']

ticker = st.selectbox("🎯 Select Ticker:", ticker_options)
custom_ticker = st.text_input("✍️ Or Enter Custom Ticker:")
if custom_ticker:
    ticker = custom_ticker.upper()

# Dates & interval
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("🗵 Start Date", datetime.date(2015, 1, 1))
with col2:
    end_date = st.date_input("🗵 End Date", datetime.date.today())

interval = st.selectbox("⏱️ Time Interval", ['1m', '5m', '1h', '1d'], index=3)

# Analyze button
if st.button("🔍 Analyze Stock"):
    with st.spinner("⚙️ Fetching and analyzing data..."):
        try:
            if interval == '1m':
                start_date = datetime.date.today() - datetime.timedelta(days=5)
            elif interval == '5m':
                start_date = datetime.date.today() - datetime.timedelta(days=30)

            df = load_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), interval)

            if df is None or df.empty:
                st.error("⚠️ No stock data found for this period.")
            else:
                df = process_indicators(df)

                if df is None or df.empty or len(df) < 14:
                    st.error("⚠️ Not enough data for indicator-based analysis. Try a different ticker or date range.")
                else:
                    df.dropna(inplace=True)

                    if df.empty:
                        st.error("⚠️ All rows dropped due to missing indicator values.")
                    else:
                        score, label = score_stock(df)
                        latest = df.iloc[-1]
                        latest_signal = latest.get('Signal', 'N/A')

                        try:
                            latest_news = fetch_recent_news(ticker)
                        except:
                            latest_news = "News not available"

                        features_required = ['RSI', 'SMA_20', 'SMA_50', 'MACD', 'Signal_Line', 'BB_High', 'BB_Low', 'ATR', 'Volume_Z']
                        features = df[features_required].tail(1).dropna()

                        prediction_label = "⚠️ Not enough data for prediction"
                        confidence = 0

                        if not features.empty and len(features.columns) == len(features_required):
                            try:
                                prediction = model.predict(features)[0]
                                confidence = max(model.predict_proba(features)[0]) * 100
                                prediction_label = "✅ High Potential" if prediction == 1 else "❌ Not High Potential"
                            except Exception as e:
                                prediction_label = f"⚠️ Prediction failed: {e}"
                                confidence = 0

                        # Summary display
                        st.subheader(f"📊 Summary for {ticker}")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("📌 Signal", latest_signal)
                        col2.metric("⭐ Score", f"{score}/7")
                        col3.metric("🎯 Confidence", f"{confidence:.2f}%" if confidence else "N/A")

                        st.markdown(
                            f"""<div style="background-color:#f9f9f9;padding:15px;border-radius:10px">
                                🏷️ <b> Rule-Based Label:</b> {label}<br>
                                🤖 <b> ML Prediction:</b> {prediction_label}<br>
                                📰 <b>Latest News:</b> {latest_news}
                            </div>""", unsafe_allow_html=True
                        )

                        try:
                            insert_signal_data(ticker, latest_signal, score, label, prediction_label, confidence, latest['Close'], latest_news)
                        except Exception as e:
                            st.warning(f"⚠️ Could not insert signal into DB: {e}")

                        st.subheader("📈 Price Info")
                        st.write({
                            "Open": round(latest['Open'], 2),
                            "High": round(latest['High'], 2),
                            "Low": round(latest['Low'], 2),
                            "Close": round(latest['Close'], 2),
                            "Volume": int(latest['Volume'])
                        })

                        st.dataframe(df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(30))

                        candle = go.Figure(data=[go.Candlestick(
                            x=df.index, open=df['Open'], high=df['High'],
                            low=df['Low'], close=df['Close'],
                            increasing_line_color='green', decreasing_line_color='red'
                        )])
                        candle.update_layout(template='plotly_white', title=f"{ticker} Candlestick Chart")
                        st.plotly_chart(candle, use_container_width=True)

                        st.subheader("📉 Signal Chart with Indicators")
                        try:
                            fib = fibonacci_levels(df)
                        except:
                            fib = None

                        try:
                            signal_fig = plotly_signals(df, title=f"{ticker} Signal Chart")
                            st.plotly_chart(signal_fig, use_container_width=True)
                        except Exception as e:
                            st.warning(f"Couldn't generate interactive signal chart: {e}")

                        st.subheader("📊 Basic Signal Chart")
                        st.plotly_chart(plotly_signals(df, title=f"{ticker} Signal Chart"), use_container_width=True, key=f"{ticker}_signal_chart")

                        if st.checkbox("🔁 Run Backtest"):
                            trades = backtest_signals(df)
                            trades_df = pd.DataFrame(trades)
                            st.dataframe(trades_df)
                            st.download_button("⬇️ Download Backtest", trades_df.to_csv(index=False), file_name=f"{ticker}_backtest.csv")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Top recommendations download
if st.button("📅 Download Top Recommendations"):
    result_df = screen_stocks(['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'TCS.NS', 'INFY.NS', 'VOO', '^NSEI'])
    if result_df is not None:
        st.download_button("⬇️ Download CSV", result_df.to_csv(index=False), file_name="top_stocks.csv")

# Sidebar: Signal history
st.sidebar.markdown("### 🕒 Signal History Viewer")
if st.sidebar.checkbox("📂 View Historical Predictions"):
    selected_ticker = st.sidebar.selectbox("Select Ticker", ticker_options + ["(All)"])
    limit = st.sidebar.slider("How many records?", 10, 100, 25)

    try:
        history_df = fetch_signal_history(ticker=None if selected_ticker == "(All)" else selected_ticker, limit=limit)
        st.subheader("📜 Prediction History")
        st.dataframe(history_df)
    except Exception as e:
        st.error(f"⚠️ Could not load history: {e}")
