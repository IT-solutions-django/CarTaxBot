from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from typing import Optional, Dict, List, Union
from datetime import datetime
from settings.static import Currency, EngineType
import aiohttp
from bs4 import BeautifulSoup
import json
from settings.static import (
    Currency, 
    CarAge, 
    CarType,
)
from settings.static import BackendURL


back_domain = BackendURL.DOMAIN.value


async def show_options(obj: Union[types.CallbackQuery, types.Message], data_dict: Dict[str, dict], exclude_key: str,
                       action: Optional[str] = None) -> None:
    builder = InlineKeyboardBuilder()
    for key in data_dict.keys():
        if action is not None:
            builder.row(types.InlineKeyboardButton(text=key, callback_data=f'{action}_{key}'))
        else:
            builder.row(types.InlineKeyboardButton(text=key, callback_data=key))

    if isinstance(obj, types.CallbackQuery):
        await obj.message.answer(text=f'Выберите {exclude_key}', reply_markup=builder.as_markup())
        await obj.answer()
    elif isinstance(obj, types.Message):
        await obj.answer(text=f'Выберите {exclude_key}', reply_markup=builder.as_markup())


async def calc_toll(price: int, age: str, volume: int, currency: str, car_type: str, engine_type: str = None):
    try:
        currency: Currency = Currency(currency)
        engine_type = EngineType(engine_type)
        age: CarAge = CarAge(age)
        car_type: CarType = CarType(car_type)

        exchange_rates = await get_exchange_rates()

        price = float(price)
        volume = int(volume)
        insurance_rus = 0

        # Перевод цены в рубли
        one_rub = exchange_rates[currency.value]['exchange_rate']
        price_rus = round(price * one_rub)

        # Таможенное оформление
        if price_rus <= 200000:
            tof = 1067
        elif (price_rus <= 450000) and (price_rus > 200000):
            tof = 2134
        elif (price_rus <= 1200000) and (price_rus > 450000):
            tof = 4269
        elif (price_rus <= 2700000) and (price_rus > 1200000):
            tof = 11746
        elif (price_rus <= 4200000) and (price_rus > 2700000):
            tof = 16524
        elif (price_rus <= 5500000) and (price_rus > 4200000):
            tof = 21344
        elif (price_rus <= 7000000) and (price_rus > 5500000):
            tof = 27540
        else:
            tof = 30000

        if car_type == CarType.PASSENGER:
            # Новые автомобили
            if age == CarAge.LESS_THAN_3:
                if volume >= 3500:
                    yts = 2285200
                elif (volume >= 3000) and (volume <= 3499):
                    yts = 1794600
                else:
                    yts = 3400
                europrice = price_rus / exchange_rates['EUR']['exchange_rate']

                if engine_type == EngineType.ELECTRO:
                    duty = europrice * 0.15
                    yts = 20000*0.17
                elif europrice < 8500:
                    duty = europrice * 0.54
                    if duty / volume < 2.5:
                        duty = volume * 2.5
                elif (europrice >= 8500) and (europrice < 16700):
                    duty = europrice * 0.48
                    if duty / volume < 3.5:
                        duty = volume * 3.5
                elif (europrice >= 16700) and (europrice < 42300):
                    duty = europrice * 0.48
                    if duty / volume < 5.5:
                        duty = volume * 5.5
                elif (europrice >= 42300) and (europrice < 84500):
                    duty = europrice * 0.48
                    if duty / volume < 7.5:
                        duty = volume * 7.5
                elif (europrice >= 84500) and (europrice < 169000):
                    duty = europrice * 0.48
                    if duty / volume < 15:
                        duty = volume * 15
                else:
                    duty = europrice * 0.48
                    if duty / volume < 20:
                        duty = volume * 20
            
            elif age == CarAge.FROM_3_TO_5:
                if volume >= 3500:
                    yts = 3004000
                elif (volume >= 3000) and (volume <= 3499):
                    yts = 2747200
                else:
                    yts = 5200
                
                europrice = price_rus / exchange_rates['EUR']['exchange_rate']
                if engine_type == EngineType.ELECTRO:
                    duty = europrice * 0.15
                    yts = 20000*0.26
                elif volume <= 1000:
                    duty = volume * 1.5
                elif (volume >= 1001) and (volume <= 1500):
                    duty = volume * 1.7
                elif (volume >= 1501) and (volume <= 1800):
                    duty = volume * 2.5
                elif (volume >= 1801) and (volume <= 2300):
                    duty = volume * 2.7
                elif (volume >= 2301) and (volume <= 3000):
                    duty = volume * 3
                else:
                    duty = volume * 3.6
            elif age == CarAge.FROM_5_TO_7 or age == CarAge.MORE_THAN_7:
                if volume >= 3500:
                    yts = 3004000
                elif (volume >= 3000) and (volume <= 3499):
                    yts = 2747200
                else:
                    yts = 5200

                europrice = price_rus / exchange_rates['EUR']['exchange_rate']
                if engine_type == EngineType.ELECTRO:
                    duty = europrice * 0.15
                    yts = 20000*0.26
                elif volume <= 1000:
                    duty = volume * 3
                elif (volume >= 1001) and (volume <= 1500):
                    duty = volume * 3.2
                elif (volume >= 1501) and (volume <= 1800):
                    duty = volume * 3.5
                elif (volume >= 1801) and (volume <= 2300):
                    duty = volume * 4.8
                elif (volume >= 2301) and (volume <= 3000):
                    duty = volume * 5
                else:
                    duty = volume * 5.7


            if engine_type == EngineType.ELECTRO:
                toll = price_rus * 0.15 + tof + yts
            else:
                toll = duty * exchange_rates['EUR']['exchange_rate'] + tof + yts

            res_rus = toll

            print(f'Таможенное оформление: {tof}')
            print(f'Утилизационный сбор: {yts}')
            print(f'Единая ставка: {duty}')
            print(f'Итого: {res_rus}')

            return round(toll)
        
        elif car_type in (CarType.QUAD_BIKE, CarType.SNOWMOBILE): 
            duty_percent = 0.05 
            nds_percent = 0.2 
            recycling_collection = 120750 

            duty = price_rus * duty_percent 
            nds = price_rus * nds_percent 

            result = duty + nds + recycling_collection + tof

            return result

        
    except Exception as e:
        print(f'Ошибка в calc_toll: {str(e)}')


async def get_exchange_rates() -> dict:
    url = "http://193.164.149.51/currencies/get-exchange-rates-from-cbr/"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                exchange_rates = {
                    currency: {
                        'exchange_rate': info['exchange_rate'], 
                        'updated_at': info['updated_at']
                    }
                    for currency, info in data.items()
                    if currency in ['JPY', 'KRW', 'CNY', 'EUR', 'USD']
                }
                print(exchange_rates)
                return exchange_rates
            else:
                raise Exception(f"Не удалось получить курсы валют. Код ответа: {response.status}")


def get_commissions(currency: Currency) -> tuple[float, float, float, float, float, float]:
    delivery = 0 
    our_commission = 0 
    broker = 0
    commission_sanctions = 0
    delivery_sanctions = 0
    insurance = 0

    match currency: 
        case Currency.JPY: 
            delivery = 120000 
            our_commission = 5000 
            broker = 100000 
            commission_sanctions = 10
            delivery_sanctions = 455000 
            insurance = 20000
        case Currency.CNY: 
            delivery = 17000 
            our_commission = 100000 
            broker = 120000 
        case Currency.KRW: 
            delivery = 1500000 
            our_commission = 100000 
            broker = 100000 
        case Currency.EUR: 
            pass 
        case Currency.USD:
            pass 
        case _: 
            raise Exception(f'Неизвестная валюта: {currency}')

    return delivery, our_commission, broker, commission_sanctions, delivery_sanctions, insurance 


async def add_new_client(telegram_id: int, name: str = None, phone: str = None) -> None:
    url = f'http://{back_domain}:8000/users/add-client/'  
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'telegram_id': telegram_id,
        'name': name,
        'phone': phone,
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 201 or 200:
                response_data = await response.json()
                print(f"Клиент успешно добавлен")
            elif response.status == 400:
                response_data = await response.json()
                print(f"Ошибка: {response_data.get('error', 'Unknown error')}")
            else:
                print(f"Неизвестная ошибка: {response.status}")


async def set_contact_data(telegram_id: int, name: str = None, phone: str = None) -> None:
    url = f'http://{back_domain}:8000/{BackendURL.SET_CONTACT_DATA.value}'  
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'telegram_id': telegram_id,
        'name': name,
        'phone': phone,
    }

    print('set_contact_data')
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 201 or 200:
                response_data = await response.json()
                print(f"Контактные данные успешно добавлены")
            elif response.status == 400:
                response_data = await response.json()
                print(f"Ошибка: {response_data.get('error', 'Неизвестная ошибка')}")
            else:
                print(f"Неизвестная ошибка: {response.status}")


async def add_client_calculation(
    telegram_id: int, price: float, age: str, engine_volume: float, currency: str, engine_type: str
) -> None:
    url = f'http://{back_domain}:8000/{BackendURL.ADD_CLIENT_CALCULATION.value}'  
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'telegram_id': telegram_id,
        'price': price,
        'age': age,
        'engine_volume': engine_volume,
        'currency': currency,
        'engine_type': engine_type,
    }

    print('add_client_calculation')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status in [200, 201]:
                response_data = await response.json()
                print(f"Расчёт успешно добавлен, ID: {response_data.get('calculation_id')}")
            elif response.status == 400:
                response_data = await response.json()
                print(f"Ошибка: {response_data.get('error', 'Неизвестная ошибка')}")
            elif response.status == 404:
                response_data = await response.json()
                print(f"Ошибка: {response_data.get('error', 'Клиент не найден')}")
            else:
                print(f"Неизвестная ошибка: {response.status}")


def format_float(number: float | str) -> str: 
    result = f"{number:_}".replace("_", " ") 
    print(result)
    return result