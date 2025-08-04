import feedparser

def fetch_recent_news(ticker_or_name):
    # Try both ticker and name-based search
    query = ticker_or_name.replace(".NS", "")  # Remove ".NS" for better results
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            return "❌ Failed to fetch news (parse error)"
        elif not feed.entries:
            return "ℹ️ No recent news available"
        else:
            return feed.entries[0].title
    except Exception as e:
        return f"❌ Error fetching news: {str(e)}"
