from telethon import TelegramClient, events
import asyncio
from binance import Client

api_key = 'kNjqHC6uvyoUc22LBZLlZpfbohxpvQAQHRLQpXh606Or8OvV8DQulhATbkMGGlSe'
api_secret = 'XL4xiY17DskdyaMKv8Q7MTW2eiksrKuLHIGE4BCj53whMy9tE5KrDZ4kLpESZhHx'

api_id = 7233499
api_hash = 'ae3e81cd552550ce66da4d2bbee1b77c'

telegram_client = TelegramClient('session_id', api_id, api_hash)
telegram_client.start()

def main():
    client = Client(api_key, api_secret)
    res = client.get_account()
    avg_price = client.get_avg_price(symbol='BNBUSDT')
    print(avg_price)
    print(client.response.headers)








#
# @client.on(events.NewMessage)
# async def my_event_handler(event):
#     if '1191110069' in str(event):
#         if "Coinbase will list" or "Coinbase Pro will list" or "Binance listing" in event.message.message:
#             if "are now available" not in event.message.message:
#                 print("found")





# client.run_until_disconnected()

