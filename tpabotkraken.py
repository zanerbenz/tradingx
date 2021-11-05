#printed total ETH and BTC balance and printed the most recent tpa ETH and BTC value
import ccxt
import config
import ccxt
import pandas as pd
from matplotlib.lines import Line2D
pd.set_option('display.max_rows', None)
import mplfinance as mpf
mpf.__version__
import numpy as np
from datetime import datetime

exchange = ccxt.kraken({
    'apiKey': config.KRAKEN_API_KEY,
    'secret': config.KRAKEN_SECRET_KEY,
})

balance = exchange.fetch_balance()
bars = exchange.fetch_ohlcv('ETH/BTC', timeframe='1d', limit=120)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df.index = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='ms', origin='unix'))
# print(balance)


balETH = balance['total']['ETH']
balBTC = balance['total']['BTC']
print(balETH)
print(balBTC)

df['stddev'] = df.close.rolling(window=20).std()
df['sma'] = df.close.rolling(window=20).mean()
df['close'] = df.close

tpa = { 'BTC' : 0.5, 'ETH' : 0.5 }

tpa['BTC'] = ((df.close - df.sma) / df.stddev + 4) / 8
tpa['ETH'] = ((df.sma - df.close) / df.stddev + 4) / 8
df['+1dev'] = df.close + 1 * df.stddev
df['-1dev'] = df.close - 1 * df.stddev

df['BTC'] = ((df.close - df.sma) / df.stddev + 4) / 8
df['ETH'] = ((df.sma - df.close) / df.stddev + 4) / 8

z = (df['BTC'].tail(1))
y = (df['ETH'].tail(1))
print(z)
print(y)

