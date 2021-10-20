#I do not know how to plot a legend onto the charts using mplfinance. I think that I need to use matplotlib to add subplots and then add legends onto them.

import ccxt
import pandas as pd
pd.set_option('display.max_rows', None)
import mplfinance as mpf
mpf.__version__
import numpy as np
from datetime import datetime

exchange = ccxt.kraken()
bars = exchange.fetch_ohlcv('ETH/BTC', timeframe='1d', limit=120)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df.index = pd.DatetimeIndex(df['timestamp'])
print(df)

#calculate the rolling standard deviation using the hourly close price of ETHBTC going back 20 periods and assign it to a variable
#calculate a 20 period simple moving average of the hourly close price of ETHBTC and assign it to a variable
#made a variable equal to the close price of the time interval that you choose

df['stddev'] = df.close.rolling(window=20).std()
df['sma'] = df.close.rolling(window=20).mean()
df['close'] = df.close

tpa = { 'BTC' : 0.5, 'ETH' : 0.5 }

tpa['BTC'] = ((df.close - df.sma) / df.stddev + 4) / 8
tpa['ETH'] = ((df.sma - df.close) / df.stddev + 4) / 8

df['+1dev'] = df.close + 1 * df.stddev
df['-1dev'] = df.close - 1 * df.stddev


ap2 = [ mpf.make_addplot(tpa['BTC'],color='g',panel=0),
        mpf.make_addplot(tpa['ETH'],color='b',panel=0),
        mpf.make_addplot(df['+1dev'],color='red',panel=1),
        mpf.make_addplot(df['-1dev'],color='red',panel=1),

      ]

mpf.plot(df,type='candle', title='Awesome_Tool',ylabel='Price with +1 and -1 \n STDEVS from the close',ylabel_lower='Volume',xrotation=90,volume=True,main_panel=1,volume_panel=2,addplot=ap2,figscale=1.1,figratio=(8,5),style='blueskies',panel_ratios=(6,5,3))

# # print(ccxt.exchanges)
#
# # for exchanges in ccxt.exchanges:
# #     print(exchanges)
#
# exchange = ccxt.kraken()
# # print(exchange)
#
# markets = exchange.load_markets()
#
# # print(markets)
#
# # ticker = exchange.fetch_ticker('ZEN/USD')
# # print(ticker)
#
# ohlc = exchange.fetch_ohlcv('ETH/BTC', timeframe='1d', limit=30)
# print(ohlc)

# for candle in ohlc:
#     print(candle)

# for market in markets:
#     print(market)

# exchange_id = 'binance'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
# })