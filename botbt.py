import ccxt
import pandas as pd
from matplotlib.lines import Line2D

pd.set_option('display.max_rows', None)
import mplfinance as mpf

mpf.__version__
import numpy as np
from datetime import datetime

exchange = ccxt.kraken()
bars = exchange.fetch_ohlcv('ETH/BTC', timeframe='1d', limit=124)
# bars = exchange.fetch_ohlcv('ETH/BTC', timeframe='1d', limit=120)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df.index = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='ms', origin='unix'))

df['stddev'] = df.close.rolling(window=20).std()
df['sma'] = df.close.rolling(window=20).mean()
df['close'] = df.close
tpa = {'tpaBTC': 0.5, 'tpaETH': 0.5}
# tpa = {'BTC': ((df.close - df.sma) / df.stddev + 4) / 8, 'ETH': ((df.sma - df.close) / df.stddev + 4) / 8}
tpa['tpaBTC'] = ((df.close - df.sma) / df.stddev + 4) / 8
tpa['tpaETH'] = ((df.sma - df.close) / df.stddev + 4) / 8
# df['+1dev'] = df.close + 1 * df.stddev
# df['-1dev'] = df.close - 1 * df.stddev
df['tpaBTC'] = ((df.close - df.sma) / df.stddev + 4) / 8
df['tpaETH'] = ((df.sma - df.close) / df.stddev + 4) / 8

startingBalance = {'BTC': 1, 'ETH': 0}
df['currentBTC'] = startingBalance['BTC'] * df['tpaBTC']
df['btcBalETH'] = startingBalance['BTC'] * df['tpaETH']
df['totalBTC'] = df['currentBTC'] + df['btcBalETH']
df['currentETH'] = df['btcBalETH'] / df['close']
df['totalBTC'] = (df['currentETH'] * df['close']) + df['currentBTC']
# a = (df['close'])
# df['btcBalETH'] = (df['currentETH'] * a)

# balETH = balance['total']['ETH']
# balBTC = balance['total']['BTC']
# btcBalETH = (balETH * a)
# totalBalBTC = btcBalETH + balBTC

# pctPortBTC = balBTC/totalBalBTC
# pctPortETH = btcBalETH/totalBalBTC

# currentETH = df
# totalBTC =
# backtestDf = df.loc[:, ['close', 'BTC', 'ETH']]
backtestDf = df.loc[:, ['close', 'tpaBTC', 'tpaETH', 'currentBTC', 'currentETH', 'totalBTC']]
# print(currentBTC)
print(backtestDf)
