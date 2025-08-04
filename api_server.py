from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Flask API for StockIQ is running."

@app.route("/top-stocks", methods=["GET"])
def top_stocks():
    top_stocks_data = [
        {
            "ticker": "AAPL",
            "companyName": "Apple Inc.",
            "price": 195.30,
            "signal": "Buy",
            "confidence": 0.92,
            "summary": "Apple shows bullish momentum supported by MACD and RSI crossover.",
            "news": [
                {"title": "Apple hits new high amid strong iPhone sales", "url": "https://example.com/apple-news"},
                {"title": "Analysts remain optimistic on Apple", "url": "https://example.com/apple-analyst"}
            ]
        },
        {
            "ticker": "TSLA",
            "companyName": "Tesla Inc.",
            "price": 755.20,
            "signal": "Sell",
            "confidence": 0.78,
            "summary": "Tesla faces resistance near 770; RSI indicates overbought zone.",
            "news": [
                {"title": "Tesla's stock dips after earnings report", "url": "https://example.com/tesla-news"},
                {"title": "Investors cautious about Tesla’s future", "url": "https://example.com/tesla-investors"}
            ]
        },
        {
            "ticker": "MSFT",
            "companyName": "Microsoft Corporation",
            "price": 340.15,
            "signal": "Hold",
            "confidence": 0.83,
            "summary": "Microsoft remains range-bound; no strong breakout or breakdown signals.",
            "news": [
                {"title": "Microsoft focuses on AI and cloud growth", "url": "https://example.com/msft-news"},
                {"title": "MSFT consolidates after recent rally", "url": "https://example.com/msft-rally"}
            ]
        }
    ]

    return jsonify(top_stocks_data)

@app.route("/stock-details", methods=["GET"])
def stock_details():
    ticker = request.args.get("ticker", "AAPL")

    # Dummy OHLCV data
    ohlcv = [
        {"date": "2025-07-23", "open": 190, "close": 200, "high": 202, "low": 188, "volume": 5000000}
    ]

    # Dummy chartData
    chartData = [
        {"date": "2025-07-23", "rsi": 55, "macd": 1.1, "bb": 180},
        {"date": "2025-07-24", "rsi": 60, "macd": 1.3, "bb": 190},
        {"date": "2025-07-25", "rsi": 65, "macd": 1.4, "bb": 210},
    ]

    return jsonify({
        "ticker": ticker,
        "ohlcv": ohlcv,
        "chartData": chartData
    })

if __name__ == "__main__":
    app.run(debug=False)
