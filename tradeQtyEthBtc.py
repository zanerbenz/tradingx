import ccxt
import config
import ccxt
import pandas as pd
from matplotlib.lines import Line2D
pd.set_option('display.max_rows', None)
import mplfinance as mpf
mpf.__version__
from decimal import Decimal

# exchange = ccxt.ftx({
#     'apiKey': config.FTXUS_API_KEY,
#     'secret': config.FTXUS_SECRET_KEY,
# })
exchange = ccxt.ftx({'apiKey': config.FTXUS_API_KEY, 'secret': config.FTXUS_SECRET_KEY, 'hostname': 'ftx.us'})

balance = exchange.fetch_balance()
bars = exchange.fetch_ohlcv('ETH/BTC', timeframe='1d', limit=120)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df.index = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='ms', origin='unix'))

recentEthBtcPrice = (df['close'].tail(1).values[0])

# balETH = balance['total']['ETH']
balBTC = balance['total']['BTC']
btcBalETH = (balance['total']['ETH'] * recentEthBtcPrice)
totalBalBTC = btcBalETH + balBTC

pctPortBTC = balBTC/totalBalBTC
pctPortETH = btcBalETH/totalBalBTC

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

# ap2 = [ mpf.make_addplot(tpa['BTC'], color='g',panel=1),
#         mpf.make_addplot(tpa['ETH'], color='b',panel=1),
#         mpf.make_addplot(df['+1dev'], color='red',panel=0),
#         mpf.make_addplot(df['-1dev'], color='red',panel=0),
#
#        ]
# fig, axes = mpf.plot(df,type='candle', title='Awesome_Tool',ylabel='Price with +1 and -1 \n STDEVS from the close',
#                      ylabel_lower='Volume',xrotation=90,volume=True,main_panel=0,volume_panel=2,addplot=ap2,
#                      figscale=1.1,figratio=(8,5),style='yahoo',panel_ratios=(6,5,3), returnfig=True)
# custom_lines = [Line2D([0], [0], color='g'),
#                 Line2D([0], [0], color='b')]
#
# axes[2].legend(custom_lines, ['BTC', 'ETH'])
# axes[0].legend(['+-1dev'])
# axes[0].set_title('ETH/BTC')
#
# mpf.show(block=True)

newTpaBTC = (df['BTC'].tail(1).values[0])
newTpaETH = (df['ETH'].tail(1).values[0])

tpaChangeETH = newTpaETH - pctPortETH



tradeQtyEthBtc = (tpaChangeETH * totalBalBTC) / recentEthBtcPrice
tradeQtyEthBtc = Decimal(str(tradeQtyEthBtc)).quantize(Decimal('0.12345'))
print(type(tradeQtyEthBtc))

print('pctPortBTC: ' + str(pctPortBTC)) #current tpa BTC
print('pctPortETH: ' + str(pctPortETH)) #current tpa ETH
print('newTpaBTC: ' + str(newTpaBTC)) #updated tpa
print('newTpaETH: ' + str(newTpaETH)) #updated tpa
print('-')
print('tpaChangeETH: ' + str(tpaChangeETH)) #difference between optimal eth tpa and the percentage of the portfolio that is currently in eth
print('tradeQtyEthBtc: ' + str(tradeQtyEthBtc)) #how much btc we need to buy or sell (if this number is + we buy ETH/BTC and if - we sell)

spread_bp = 25
spread_pct = spread_bp / 100
spread_ratio = spread_pct / 100
print('spread_ratio: ' + str(spread_ratio))
print('recentEthBtcPrice: ' + str(recentEthBtcPrice))



if tradeQtyEthBtc > 0:
    price_mult = 1 + spread_ratio
    print('price_mult: ' + str(price_mult))
    order = exchange.create_order('ETH/BTC', 'limit', 'buy', tradeQtyEthBtc, recentEthBtcPrice * price_mult)
else:
    price_mult = 1 - spread_ratio
    print('price_mult: ' + str(price_mult))
    order = exchange.create_order('ETH/BTC', 'limit', 'sell', tradeQtyEthBtc * -1, recentEthBtcPrice * price_mult)

print(order)



