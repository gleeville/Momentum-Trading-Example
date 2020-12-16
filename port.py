import alpaca_trade_api as tradeapi
import requests
import time
from ta import macd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import json

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
min_share_price = 5.0
max_share_price = 20.0
# Minimum previous-day dollar volume for a stock we might consider
min_last_dv = 500000
# Stop limit to default to
default_stop = .95
# How much of our portfolio to allocate to any one position
risk = 0.001



#set the group of stocks to look at
stockUniverse = ['TSLA', 'GM']
api.allStocks = []
for stock in stockUniverse:
  api.allStocks.append([stock, 0])

api.long = []
api.short = []
api.qShort = None
api.qLong = None
api.adjustedQLong = None
api.adjustedQShort = None
api.blacklist = set()
api.longAmount = 0
api.shortAmount = 0
api.timeToClose = None

def getPercentChanges():
  length = 10
  for i, stock in enumerate(api.allStocks):
    bars = api.get_barset(stock[0], 'minute', length)
    api.allStocks[i][1] = (bars[stock[0]][len(bars[stock[0]]) - 1].c - bars[stock[0]][0].o) / bars[stock[0]][0].o
    print("10 Min price move "+ str(stock))

def getMove(symbol, length):
    bars = api.get_barset(symbol, 'minute', length)
    print("Bars are \n " + str(bars) + "\n")
    move = (bars[symbol][len(bars[symbol]) - 1].c - bars[symbol][0].o) / bars[symbol][0].o
    print(str(symbol) + " Open price " + str(bars[symbol][0].o) + " at " + str(bars[symbol][0].t) + "\n" + str(symbol) + " Close price " + str(bars[symbol][len(bars[symbol]) - 1].c) + " at " + str(bars[symbol][len(bars[symbol]) - 1].t) + "\n")
    return(move)

#Get the daily move from low to high for n days
def getIntraDayMove(symbol, days):
    bars = api.get_barset(symbol, 'day', days)
    i = 0
    move={}
    while i < len(bars[symbol]):
        move[i] = (bars[symbol][i].h - bars[symbol][i].l)/ bars[symbol][i].l
        pct = "{:.2%}".format(move[i])
        #This line is debug code to see output in readable format
        print("day " + str(i + 1) + " intra day move " + pct)
        i += 1
    return (move)

def markPort():
    totalMark=0
    positions = api.list_positions()
    for position in positions:
        lastPrice = api.get_last_trade(position.symbol).price
        totalMark = totalMark + (abs(float(position.qty)) * lastPrice)
    print("Portfolio mark is $" + str(totalMark) + "\n\n\n ")

def holdings():
    existing_positions=api.list_positions()
    for positions in existing_positions:
        if(int(positions.qty) < 0):
            print (positions.qty + " short position in " + positions.symbol)
        else:
            print (positions.qty + " long position in " + positions.symbol)
    return ()

def closeout():
    #start by cancelling open orders
    existing_orders=api.list_orders()
    for order in existing_orders:
        print("Cancelling open order in " + order.symbol)
        api.cancel_order(order.id)
    #now send trades to close out open positions. Adjust side for position.
    existing_positions=api.list_positions()
    for positions in existing_positions:
        if(int(positions.qty) < 0):
            api.submit_order(positions.symbol, positions.qty, "buy", "market", "day")
            print("Closout short " + positions.symbol + "buying " + positions.qty)
        else:
            api.submit_order(positions.symbol, positions.qty, "sell", "market", "day")
            print("Closout long " + positions.symbol + "selling " + positions.qty)
    return()

def getTickers():
    print("Getting ticker data ")
    tickers = api.polygon.all_tickers()
    print("Got em ")
    assets = api.list_assets()
    symbols = [asset.symbol for asset in assets if asset.tradable]
    return [ticker for ticker in tickers if (
        ticker.ticker in symbols and
        ticker.lastTrade['p'] >= min_share_price and
        ticker.lastTrade['p'] <= max_share_price and
        ticker.prevDay['v'] * ticker.lastTrade['p'] > min_last_dv and
        ticker.todaysChangePerc >= 3.5
    )]

markPort()
holdings()
closeout()
print("\n\n Price moves for universe are")
getPercentChanges()

print("And TTD move is " + str(getMove("TTD", 10)) + "\n\n")

print("\n\n" + str(getIntraDayMove('TTD', 20)))


print("Got this many " + str(len(getTickers())))

#g = ta.sma(getIntraDayMove('TTD', 20))
