from __future__ import print_function
from telethon import TelegramClient, events
from binance import Client
from pycoingecko import CoinGeckoAPI
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import re
import requests

binance_api_key = 'UienLKHwrf4dulShFoGDNJfkGKyDj73zYJ00i4LTjh8DopNLuNpUP2PIgxLZ6dqY'
binance_api_secret = 'rHmqQKP1KXs7M3gkcL5B9nBFqEI5gSuwHDQB65LZ3Qcx6kn5106NXPuCuge8Nzn9'

telegram_api_id = 7233499
telegram_api_hash = 'ae3e81cd552550ce66da4d2bbee1b77c'

telegram_client = TelegramClient('session_id', telegram_api_id, telegram_api_hash)
telegram_client.start()

cg = CoinGeckoAPI()

final_list_of_coins = []


@telegram_client.on(events.NewMessage)
async def my_event_handler(event):
    if '1191110069' in str(event):
        if "Coinbase will list" or "Coinbase Pro will list" or "Binance listing" in event.message.message:
            if "now available" not in event.message.message:
                list_of_symbols = re.findall(r'#\w+', event.message.message)
                if "#Binance" in list_of_symbols:
                    print("Binance here")
                    remove_tag(list_of_symbols)
                    print(final_list_of_coins)
                    for coin in final_list_of_coins:
                        get_coin_by_id(coin)
                if "#Coinbase" in list_of_symbols:
                    print("Coinbase here")
                    remove_tag(list_of_symbols)
                    print(final_list_of_coins)
                    for coin in final_list_of_coins:
                        get_coin_by_id(coin)
                    # buy_order_binance(list_of_symbols)
                if "#CoinbasePro" in list_of_symbols:
                    print("CoinbasePro here")
                    remove_tag(list_of_symbols)
                    print(final_list_of_coins)
                    for coin in final_list_of_coins:
                        get_coin_by_id(coin)


def remove_tag(list_of_symbols):
    for word in list_of_symbols[:len(list_of_symbols) - 2]:
        word = word.replace("#", "")
        final_list_of_coins.append(word)


def get_coin_by_id(coin):
    for a in cg.get_coins_list():
        if a["symbol"] == coin.lower():
            coin_symbol = a["id"]
            get_list_of_exchanges(coin, coin_symbol)


def get_list_of_exchanges(coin, coin_symbol):
    list_of_exchanges = []
    for i in cg.get_coin_by_id(id=coin_symbol)["tickers"]:
        if i["market"]["name"] not in list_of_exchanges:
            list_of_exchanges.append(i["market"]["name"])

    if "Gate.io" in list_of_exchanges:
        buy_order_gateio(coin)




def buy_order_gateio(coin):
    configuration = gate_api.Configuration(
        host="https://api.gateio.ws/api/v4",
        key="89ff6684f637400979e9e064d3d41955",
        secret="5d9002df05a03bf11d9a06940b603263a5ff9dabeea27cbcd602c51a20db20aa"
    )

    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/spot/order_book'
    query_param = f'currency_pair={coin.upper()}_USDT'
    print(query_param)
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    coin_price = r.json()["asks"][2][0]
    amount_coins_to_buy = round(1000 / float(coin_price), 2)
    print(coin_price)
    print(amount_coins_to_buy)

    api_client = gate_api.ApiClient(configuration)

    api_instance = gate_api.SpotApi(api_client)
    order = gate_api.Order(currency_pair=f"{coin.lower}_usdt", amount=str(amount_coins_to_buy), price=coin_price, side="buy")

    try:
        # Create an order
        api_response = api_instance.create_order(order)
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->create_order: %s\n" % e)


def buy_order_binance(coin):
    client = Client(binance_api_key, binance_api_secret)
    avg_price = client.get_avg_price(symbol=coin + 'USDT')
    amount_of_coins = round(1000 / int(float(avg_price["price"])), 2)
    print(amount_of_coins)
    order = client.order_market_buy(symbol=coin + 'USDT', quantity=amount_of_coins, newOrderRespType="FULL")
    print(order)
    final_list_of_coins = []


telegram_client.run_until_disconnected()

# -------------------------------------------
# Example:
# 🔥Coinbase will list: ((AXS)) ((REQ)) ((TRU)) ((QUICK)) ((WLUNA))
# 🔥 Axie Infinity (AXS), Request (REQ), TrueFi (TRU), Quickswap (QUICK) and Wrapped Luna (WLUNA) are now available on… (https://twitter.com/coinbase)
#
# #AXS #REQ #TRU #QUICK #WLUNA #Coinbase #Listing
#
# 🔥Coinbase Pro will list: ((AXS)) ((REQ)) ((TRU)) ((WLUNA))
# 🔥 Axie Infinity (AXS), Request (REQ), TrueFi (TRU) and Wrapped Luna (WLUNA) are launching on Coinbase Pro (https://twitter.com/coinbase)
#
#
# -------------------------------------------
