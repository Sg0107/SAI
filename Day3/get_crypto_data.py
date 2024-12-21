import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

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
    filename=f"{t_f}_{symname}.csv"
    df.to_csv(f"{t_f}_{symname}.csv",index = False)
    return filename
