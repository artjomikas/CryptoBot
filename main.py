from __future__ import print_function
import hashlib
import hmac
import json
import re
import time
import requests
from pycoingecko import CoinGeckoAPI
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telethon import TelegramClient, events

telegram_api_id = 7233499
telegram_api_hash = 'ae3e81cd552550ce66da4d2bbee1b77c'

telegram_client = TelegramClient('session_id', telegram_api_id, telegram_api_hash)
telegram_client.start()

cg = CoinGeckoAPI()
coins_list = cg.get_coins_list()


@telegram_client.on(events.NewMessage)
async def my_event_handler(event):
    if '1124574831' in str(event):
        do_check(event)


def do_check(event):
    if "Coinbase will list" in event.message.message or "Coinbase Pro will list" in event.message.message or "Binance listing" in event.message.message:
        if "now available" not in event.message.message:
            list_of_coins = re.findall(r'#\w+', event.message.message)
            for coin in list_of_coins[:-2]:
                buy_order_gateio(get_price(coin[1:]), list_of_coins, coin[1:])


def get_price(coin):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": coin,
        "convert": "USD"
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'eef1c752-ca36-48d0-84d3-f7035343a8cc',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        return json.loads(response.text)["data"][coin]["quote"]["USD"]["price"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def gen_sign(method, url, query_string=None, payload_string=None):
    key = 'API KEY FROM GATE IO'
    secret = 'API SECRET KET FROM GATE IO'
    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}


def buy_order_gateio(price, list_of_coins, coin):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/spot/order_book'
    url1 = '/spot/orders'
    query_param1 = ''
    query_param = f'currency_pair={coin}_USDT'
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    try:
        coin_price = r.json()["asks"][1][0]
        amount = round(1000 / (len(list_of_coins) - 2) / float(coin_price), 2)
        if ((float(coin_price) - float(price)) / float(price) * 100) < 25:
            print(coin_price)
            body = '{"currency_pair":"%s_USDT", "side":"buy", "amount":"%s","price":"%s"}' % (coin, amount, coin_price)
            sign_headers = gen_sign('POST', prefix + url1, query_param1, body)
            headers.update(sign_headers)
            r = requests.request('POST', host + prefix + url1, headers=headers, data=body)
            print(r.json())
    except KeyError:
        print(coin + " not in Gate.io")


telegram_client.run_until_disconnected()
