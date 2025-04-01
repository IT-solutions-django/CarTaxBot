from aiogram import Bot, Dispatcher
from dotenv import load_dotenv 
import asyncio
import os
from handlers import command_handler, callback_handler
from aiogram.client.default import DefaultBotProperties
from cachetools import TTLCache
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup
from settings.static import Currency
import pytz


vladivostok_tz = pytz.timezone('Asia/Vladivostok')



load_dotenv()


API_TOKEN: str = os.getenv('API_TOKEN')
bot: Bot = Bot(
    token=API_TOKEN, 
    default=DefaultBotProperties(parse_mode='Markdown')
)
dp: Dispatcher = Dispatcher()

exchange_rates_cache = TTLCache(maxsize=1, ttl=3600)
 

async def get_rates():
    """Получить валют"""
    if "exchange_rates" in exchange_rates_cache:
        print('Получили из кэша')
        print(exchange_rates_cache["exchange_rates"])
        return exchange_rates_cache["exchange_rates"]
    else:
        print('Получили из ЦБ')
        return await update_exchange_rates()

async def update_exchange_rates():
    """Обновить курсы валют"""
    url = 'https://www.cbr.ru/currency_base/daily/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status() 
            html = await response.text() 

    soup = BeautifulSoup(html, 'lxml')
    updates = dict()

    updated_at = datetime.now(vladivostok_tz).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    for currency in Currency:
        tr_element = soup.find(lambda tag: tag.name == "tr" and tag.find("td", string=currency.value))
        if tr_element:
            _, curr_code, quantity, _, exchange_rate_raw = map(lambda x: x.text, tr_element.find_all('td'))
            exchange_rate = float(exchange_rate_raw.replace(',', '.')) / int(quantity)

            updates[currency.value] = {
                'exchange_rate': exchange_rate, 
                'updated_at': updated_at,
            }

    if updates:
        exchange_rates_cache["exchange_rates"] = updates
        print('Курсы валют обновлены')
        return updates
    

async def main() -> None:
    dp.include_router(callback_handler.router)
    dp.include_router(command_handler.router)
    await dp.start_polling(bot, skip_updates=True)



if __name__ == "__main__":
    asyncio.run(main())