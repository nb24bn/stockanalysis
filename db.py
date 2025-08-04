import psycopg2
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="smartstock",
        user="postgres",        
        password="postgres"  
    )

def insert_signal_data(ticker, signal, score, label, prediction, confidence, close, news):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO stock_signals (
                ticker, signal, score, label,
                prediction, confidence, close_price, news_headline
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Convert NumPy types to native Python types
        values = (
            str(ticker),
            str(signal),
            int(score),
            str(label),
            str(prediction),
            float(confidence),
            float(close),
            str(news)
        )

        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Inserted signal for {ticker}")
    except Exception as e:
        print(f"❌ Error inserting signal: {e}")
    finally:
        cursor.close()
        conn.close()
        
def fetch_signal_history(ticker=None, limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    if ticker:
        cursor.execute("""
            SELECT timestamp, ticker, signal, score, label, prediction, confidence, close_price, news_headline
            FROM stock_signals
            WHERE ticker = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """, (ticker, limit))
    else:
        cursor.execute("""
            SELECT timestamp, ticker, signal, score, label, prediction, confidence, close_price, news_headline
            FROM stock_signals
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
    
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    cursor.close()
    conn.close()
    return df

