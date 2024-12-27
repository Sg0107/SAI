import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

def RSI(data,window):
    close_data = data['close']
    delta = close_data.diff()
    gain = delta.where(delta>0,0)
    loss = -delta.where(delta<0,0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
     # For the rest of the periods, use the smoothing formula
    for i in range(window, len(data)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (window-1) + gain.iloc[i]) / window
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (window-1) + loss.iloc[i]) / window
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    data['rsi'] = rsi
    return data

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

def Ema(data,period):
    close = data['close']
    ema = close.ewm(span=period,adjust=False).mean()
    data[f'EMA{period}'] = ema
    return data