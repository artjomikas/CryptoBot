from telethon import TelegramClient, events
from binance import Client
import re

binance_api_key = ''
binance_api_secret = ''

telegram_api_id = 7233499
telegram_api_hash = 'ae3e81cd552550ce66da4d2bbee1b77c'

telegram_client = TelegramClient('session_id', telegram_api_id, telegram_api_hash)
telegram_client.start()


@telegram_client.on(events.NewMessage)
async def my_event_handler(event):
    if '1191110069' in str(event):
        if "Coinbase will list" or "Coinbase Pro will list" or "Binance listing" in event.message.message:
            if "are now available" not in event.message.message:
                list_of_symbols = re.findall(r'#\w+', event.message.message)
                if "#Binance" in list_of_symbols:
                    print("Binance here")
                    print(list_of_symbols[0:list_of_symbols.index("#Binance")])
                    # buy_order()
                if "#Coinbase" in list_of_symbols:
                    print("Coinbase here")
                    print(list_of_symbols[0:list_of_symbols.index("#Coinbase")])
                    # buy_order()
                if "#CoinbasePro" in list_of_symbols:
                    print("CoinbasePro here")
                    print(list_of_symbols[0:list_of_symbols.index("#CoinbasePro")])
                    # buy_order()


def buy_order(symbol):
    client = Client(binance_api_key, binance_api_secret)
    avg_price = client.get_avg_price(symbol='USDT')
    print(avg_price)
    print(client.response.headers)


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