import alpaca_trade_api as tradeapi
import requests
import time
#from ta import macd
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
stockUniverse = ['TTD']
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

def getMove(symbol, length):
    bars = api.get_barset(symbol, "minute", length)
    #print("Bars are \n " + str(bars) + "\n")
    print("\n" + str(length) + " minute bar for period starting " + str(bars[symbol][0].t))
    print("Open "+ str(bars[symbol][0].o) )
    print("Close "+ str(bars[symbol][0].c) )
    print("High "+ str(bars[symbol][0].h) )
    print("Low "+ str(bars[symbol][0].l) )
    #move = (bars[symbol][len(bars[symbol]) - 1].c - bars[symbol][len(bars[symbol])].o) / bars[symbol][len(bars[symbol].o)
    move = (bars[symbol][0].c - bars[symbol][0].o) / bars[symbol][0].o
    print("Move was " + str(move) + "\n\n")
    #print(str(symbol) + " Open price the bar " + str(bars[symbol][0].o) + " at " + str(bars[symbol][0].t) + "\n" + str(symbol))
    #print(" Close the bar price " + str(bars[symbol][len(bars[symbol]) - 1].c) + " at " + str(bars[symbol][len(bars[symbol]) - 1].t) + "\n")
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

h_move = {}
now_move = {}

#Get the recent historical daily high/low move of the stock for refernce
h_move=getIntraDayMove('TTD', 5)

#print("Daily move is \n" + str(h_move))
#print("Last 5 minute move is \n" + str(now_move))

move_record={}

i = 0
while True:
    print("Time now is " + str(time.localtime(time.time())))
    print("Current market is Bid " + str(api.get_last_quote('TTD').bidprice) + " Offer " + str(api.get_last_quote('TTD').askprice) + " and last trade at " + str(api.get_last_trade('TTD').price))
    #print("Last trade details :" + str(api.get_last_trade('TTD')))
    now_move = getMove('TTD', 1)
    move_record[i]=now_move
    i += 1
    print("Incriment val is " + str(i))
    j=0
    while j < len(move_record):
        #mv = "{:.4%}".format(move_record[j])
        #print("Record " + str(j) + " Change= " + str(move_record[j]) + " ")
        print("Record " + str(j) + " Change= " + str(move_record[j]) + " ")
        j += 1
    print("Napping .... \n")
    time.sleep(60)
