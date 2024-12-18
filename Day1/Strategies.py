import pandas as pd
def trading_strategy_1(data,stop_loss,time):
    trades=[]
    in_trade = False
    buying_price = None
    buy_time = None
    reason = None
    for i, row in data.iterrows():
        if not in_trade:
            if row['close'] <= row['lower_bollinger_band'] :
                buying_price = row['close']
                buy_time = row['timestamp']
                in_trade = True
                print(f"Bought at {buying_price} on {buy_time}")

        elif in_trade:
            if row['close'] >= row['middle_bollinger_band']:
                sell_time = row['timestamp']
                selling_price = row['close']
                profit = selling_price - buying_price
                if profit > 0:
                    reason = 2
                else:
                    reason = 1
                trades.append([buy_time, buying_price, sell_time, selling_price, profit, reason])
                in_trade = False  # Exiting the trade
                print(f"Sold at {selling_price} on {sell_time} (Profit: {profit})")
                print(reason)
            # Stop-loss condition: Close price < buying price - stop loss
            elif row['close'] < buying_price - stop_loss*buying_price:
                sell_time = row['timestamp']
                selling_price = row['close']
                loss = selling_price - buying_price
                reason = 0
                trades.append([buy_time, buying_price, sell_time, selling_price, loss, reason])
                in_trade = False  # Exiting the trade
                print(f"Sold at {selling_price} on {sell_time} (Loss: {loss})")
                print(reason)
    trades_df = pd.DataFrame(trades, columns=['Buy Time', 'Buy Price', 'Sell Time', 'Sell Price', 'Profit/Loss', 'Reason'])
    trades_df.to_csv(f"Result_{time}_1.csv")

def trading_strategy_2(data,stop_loss,time):
    trades=[]
    in_trade = False
    buying_price = None
    buy_time = None
    for i, row in data.iterrows():
        if not in_trade:
            if row['EMA9'] <= row['EMA20']:
                buying_price = row['close']
                buy_time = row['timestamp']
                in_trade = True
                print(f"Bought at {buying_price} on {buy_time}")

        elif in_trade:
            if row['EMA9'] > row['EMA20']:
                sell_time = row['timestamp']
                selling_price = row['close']
                profit = selling_price - buying_price
                if profit > 0:
                    reason = 2
                else:
                    reason = 1
                trades.append([buy_time, buying_price, sell_time, selling_price, profit,reason])
                in_trade = False  # Exiting the trade
                print(f"Sold at {selling_price} on {sell_time} (Profit: {profit})")
                print(reason)
            # Stop-loss condition: Close price < buying price - stop loss
            elif row['close'] < buying_price - stop_loss*buying_price:
                sell_time = row['timestamp']
                selling_price = row['close']
                loss = selling_price - buying_price
                reason = 0
                trades.append([buy_time, buying_price, sell_time, selling_price, loss,reason])
                in_trade = False  # Exiting the trade
                print(f"Sold at {selling_price} on {sell_time} (Loss: {loss})")
                print(reason)
    trades_df = pd.DataFrame(trades, columns=['Buy Time', 'Buy Price', 'Sell Time', 'Sell Price', 'Profit/Loss','Reason'])
    trades_df.to_csv(f"Result_{time}_2.csv")
