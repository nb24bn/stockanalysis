def backtest_signals(df, initial_balance=100000):
    balance = initial_balance
    position = 0  # Number of shares held
    entry_price = 0
    trades = []

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]
        close_price = df['Close'].iloc[i]

        # BUY logic
        if signal == 'BUY' and position == 0:
            position = balance // close_price  # buy whole shares
            entry_price = close_price
            balance -= position * entry_price
            trades.append({'Date': df.index[i], 'Action': 'BUY', 'Price': entry_price})

        # SELL logic
        elif signal == 'SELL' and position > 0:
            sell_price = close_price
            balance += position * sell_price
            profit = (sell_price - entry_price) * position
            trades.append({'Date': df.index[i], 'Action': 'SELL', 'Price': sell_price, 'Profit': profit})
            position = 0  # reset

    # Final report
    final_value = balance + (position * df['Close'].iloc[-1])
    total_return = final_value - initial_balance
    return_pct = (total_return / initial_balance) * 100
    win_trades = [t for t in trades if 'Profit' in t and t['Profit'] > 0]
    loss_trades = [t for t in trades if 'Profit' in t and t['Profit'] < 0]

    print(f"\n📊 BACKTEST SUMMARY:")
    print(f"Initial Balance: ₹{initial_balance:,.2f}")
    print(f"Final Balance: ₹{final_value:,.2f}")
    print(f"Total Return: ₹{total_return:,.2f} ({return_pct:.2f}%)")
    print(f"Total Trades: {len([t for t in trades if t['Action'] == 'SELL'])}")
    print(f"Winning Trades: {len(win_trades)} | Losing Trades: {len(loss_trades)}")

    return trades
