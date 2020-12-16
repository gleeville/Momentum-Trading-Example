import alpaca_trade_api as tradeapi
import requests
import time
# from ta import macd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import json

# Replace these with your API connection info from the dashboard
base_url = 'https://paper-api.alpaca.markets'
api_key_id = 'PKFJXDVKD1LK2F3JGWH9'
api_secret = '8aUP4cGiK3NWKyQBRcAhFwAlIjeK3hVgXvm0Gtr9'

api = tradeapi.REST(
    base_url=base_url,
    key_id=api_key_id,
    secret_key=api_secret
)

session = requests.session()
positions = {}
qty = {}
assets = {}
price={}
near={}
far={}

# We only consider stocks with per-share prices inside this range
min_share_price = 2.0
max_share_price = 13.0
# Minimum previous-day dollar volume for a stock we might consider
min_last_dv = 500000
# Stop limit to default to
default_stop = .95
# How much of our portfolio to allocate to any one position
risk = 0.001


def closeout():
    existing_orders=api.list_orders()
    for order in existing_orders:
        api.cancel_order(order.id)
    return()

def buy_mkt_day(symbol, qty):
    print('Buying' + symbol)
    api.submit_order(symbol, qty, "buy", "market", "day")
    return()

def buyLmtDay(symbol, qty):
    print('Limit Buying '+symbol)
    near = getBidPrice(symbol)
    api.submit_order(symbol, qty, "buy", "limit", "day", near)
    return()

def execLmtOrd(symbol, qty, side):
    far = getFarPrice(symbol, side)
    if(side == 'buy'):
        print("Buying " + symbol + "at " + str(far))
        api.submit_order(symbol, qty, side, "limit", "day", far)
    else:
        print("Selling " + symbol + "at " + str(far))
        api.submit_order(symbol, qty, side, "limit", "day", far)
    return()

def getAskPrice(stock):
    price = api.get_last_quote(stock).askprice
    return(price)

def getBidPrice(stock):
    price = api.get_last_quote(stock).bidprice
    return(price)

def getFarPrice(stock, side):
    if(side == 'buy'):
        price = api.get_last_quote(stock).askprice
    else:
        price = api.get_last_quote(stock).bidprice
    return(price)

def holdings():
    existing_positions=api.list_positions()
    for positions in existing_positions:
        print ('   ')
    return (positions.symbol, positions.qty)

def get_last_price():
    holdings()
    return

def get_tickers():
    print('Getting current ticker data...')
    tickers = api.polygon.all_tickers()
    print('Success.')
    assets = api.list_assets()
    symbols = [asset.symbol for asset in assets if asset.tradable]
    return (tickers)

#    return [ticker for ticker in tickers if (
#        ticker.ticker in symbols and
#        ticker.lastTrade['p'] >= min_share_price and
#        ticker.lastTrade['p'] <= max_share_price and
#        ticker.prevDay['v'] * ticker.lastTrade['p'] > min_last_dv and
#        ticker.todaysChangePerc >= 3.5
#    )]

#
#
#WORK NEEDED HERE##############
def getOut():
    holdings()
    existing_position=api.cancel_order(symbol)
    return()

print ('running')

# print(api.get_account())
print ('  ')
# print(api.last_order())

# print(api.get_position('TSLA'))
print('Submitting trades')

#buy_mkt_day('TSLA', 100)
#buyLmtDay('TSLA', 100)
execLmtOrd('TSLA', 100, 'buy')

time.sleep(5)
print ('cancelling open orders')
closeout()

print ('Open Positions')
print(holdings())

#print ('Closing Positions')
#getOut()

#print ('Tickers')
#print(get_tickers())

print ('Ask Price ')
print (getAskPrice('TSLA'))

print ('Bid Price')
print (getBidPrice('TSLA'))

print ('Get far')
print (getFarPrice('TSLA', 'buy'))

print ('Done')
