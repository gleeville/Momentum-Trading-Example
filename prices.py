import alpaca_trade_api as tradeapi
import threading
import time
import datetime

API_KEY = "PKFJXDVKD1LK2F3JGWH9"
API_SECRET = "8aUP4cGiK3NWKyQBRcAhFwAlIjeK3hVgXvm0Gtr9"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"


api = tradeapi.REST(
    base_url=base_url,
    key_id=api_key_id,
    secret_key=api_secret
)

session = requests.session()
positions = {}
qty = {}
assets = {}
price = {}
