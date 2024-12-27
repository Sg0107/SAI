from Indicators import bollinger_bands
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
from binance.client import Client
from twilio.rest import Client
exchange = ccxt.binance()
def get_data(start, end, t_f, sym,symname):
    start_timestamp = int(start.timestamp()*1000)
    end_timestamp = int(end.timestamp()*1000)
    ohlc_data = []
    while start_timestamp <= end_timestamp :
        ohlcv = exchange.fetch_ohlcv(sym, t_f, start_timestamp)
        ohlc_data.extend(ohlcv)
        start_timestamp = ohlcv[-1][0] + exchange.parse_timeframe(t_f) * 1000
    df = pd.DataFrame(ohlc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    return df
def bollinger_bands(data,window,num_std_dev):
    close_data = data['close']
    sma = close_data.rolling(window = window).mean()
    rolling_std = close_data.rolling(window=window).std()
    upper_band = sma + rolling_std*num_std_dev
    lower_band = sma - rolling_std*num_std_dev
    data['upper_bollinger_band'] = upper_band
    data['middle_bollinger_band'] = sma
    data['lower_bollinger_band'] = lower_band
    return data


end_date = datetime.now()  # Current time
start_date = end_date - timedelta(days=7)
timeframe = '1h'  # Example: 1-hour candles
symbol = 'BTC/USDT'  # Example: Bitcoin to USDT pair
symbol_name = 'BTCUSDT'  # Symbol name for file or display (if needed)

# Fetch data for the last 7 days
df = get_data(start_date, end_date, timeframe, symbol, symbol_name)
bollinger_data = bollinger_bands(df,20,1.94937)
lower_band = bollinger_data['lower_bollinger_band'].iloc[-1]
current_price = bollinger_data['close'].iloc[-1]
upper_band = bollinger_data['upper_bollinger_band'].iloc[-1]
message = "yes"
if current_price <= lower_band:
    # Twilio credentials
    message = f"Bitcoin price has touched the lower Bollinger Band at ${current_price:.2f}."
    account_sid = 'AC03ada41c6e6127b8756cf59f227056d1'
    auth_token = '31140d2ca92eb922ce0b9b6ae330431a'
    client = Client(account_sid, auth_token)

    whatsapp_message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Twilio's WhatsApp sandbox number
        to='whatsapp:+918440096915'  # Your verified WhatsApp number
    )

    print("Message sent")   
elif upper_band <= current_price:
    message = f"Bitcoin price has touched the upper Bollinger Band at ${current_price:.2f}."
    account_sid = 'AC03ada41c6e6127b8756cf59f227056d1'
    auth_token = '31140d2ca92eb922ce0b9b6ae330431a'
    client = Client(account_sid, auth_token)

    whatsapp_message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Twilio's WhatsApp sandbox number
        to='whatsapp:+918440096915'  # Your verified WhatsApp number
    )

    print("Message sent") 
else: 
    message = "No"
    account_sid = 'AC03ada41c6e6127b8756cf59f227056d1'
    auth_token = '31140d2ca92eb922ce0b9b6ae330431a'
    client = Client(account_sid, auth_token)

    whatsapp_message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Twilio's WhatsApp sandbox number
        to='whatsapp:+918440096915'  # Your verified WhatsApp number
    )

    print("Message sent") 