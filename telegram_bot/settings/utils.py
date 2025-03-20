from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from typing import Optional, Dict, List, Union
from datetime import datetime
from settings.static import Currency, EngineType
import aiohttp
from bs4 import BeautifulSoup
import json
from settings.static import Currency



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


def calc_toll(price: int, age: int, volume: int, currency: str, engine_type: str = None):
    try:
        currency: Currency = Currency(currency)
        engine_type = EngineType(engine_type)
        delivery, our_commission, broker, commission_sanctions, delivery_sanctions, insurance = get_commissions(currency=currency)

        exchange_rates = {
            'JPY': 0.6258, 
            'KRW': 0.0665, 
            'CNY': 11.4265,
            'EUR': 87.57,
        }

        price = float(price)
        volume = int(volume)
        age = int(age)
        commision_sanctions_ = 0
        insurance_rus = 0

        # Перевод цены в рубли
        one_rub = exchange_rates[currency.value]
        price_rus = round(price * one_rub)

        if currency == Currency.JPY:             
            # Санкционные авто
            if (volume > 1800 or engine_type == EngineType.HYBRID or engine_type == EngineType.ELECTRO):
                commision_sanctions_ = price * commission_sanctions / 100
                price_rus = round((price + commision_sanctions_) * one_rub)
                delivery = delivery_sanctions
            else:
                price_rus = round(price * one_rub)
                insurance_rus = round(insurance * one_rub)

        # Таможенное оформление
        if price_rus < 200000:
            tof = 1067
        elif (price_rus < 450000) and (price_rus >= 200000):
            tof = 2134
        elif (price_rus < 1200000) and (price_rus >= 450000):
            tof = 4269
        elif (price_rus < 2700000) and (price_rus >= 1200000):
            tof = 11746
        elif (price_rus < 4200000) and (price_rus >= 2700000):
            tof = 16524
        elif (price_rus < 5500000) and (price_rus >= 4200000):
            tof = 21344
        elif (price_rus < 7000000) and (price_rus >= 5500000):
            tof = 27540
        else:
            tof = 30000

        print(f'Таможенное оформление: {tof}')

        age 
        if age <= 3:
            if volume >= 3500:
                yts = 2285200
            elif (volume >= 3000) and (volume <= 3499):
                yts = 1794600
            else:
                yts = 3400
            evroprice = price_rus / exchange_rates['EUR']
            if engine_type == EngineType.ELECTRO:
                duty = evroprice * 0.15
                yts = 20000*0.17
            elif evroprice < 8500:
                duty = evroprice * 0.54
                if duty / volume < 2.5:
                    duty = volume * 2.5
            elif (evroprice >= 8500) and (evroprice < 16700):
                duty = evroprice * 0.48
                if duty / volume < 3.5:
                    duty = volume * 3.5
            elif (evroprice >= 16700) and (evroprice < 42300):
                duty = evroprice * 0.48
                if duty / volume < 5.5:
                    duty = volume * 5.5
            elif (evroprice >= 42300) and (evroprice < 84500):
                duty = evroprice * 0.48
                if duty / volume < 7.5:
                    duty = volume * 7.5
            elif (evroprice >= 84500) and (evroprice < 169000):
                duty = evroprice * 0.48
                if duty / volume < 15:
                    duty = volume * 15
            else:
                duty = evroprice * 0.48
                if duty / volume < 20:
                    duty = volume * 20
        
        elif (age > 3) and (age <= 5):
            if volume >= 3500:
                yts = 3004000
            elif (volume >= 3000) and (volume <= 3499):
                yts = 2747200
            else:
                yts = 5200
            
            evroprice = price_rus / exchange_rates['EUR']
            if engine_type == EngineType.ELECTRO:
                duty = evroprice * 0.15
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
        elif age > 5:
            if volume >= 3500:
                yts = 3004000
            elif (volume >= 3000) and (volume <= 3499):
                yts = 2747200
            else:
                yts = 5200

            evroprice = price_rus / exchange_rates['EUR']
            if engine_type == EngineType.ELECTRO:
               duty = evroprice * 0.15
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
            toll = duty * exchange_rates['EUR'] + tof + yts

        res_rus = toll  + (delivery*one_rub) + our_commission + broker + insurance_rus

        print(f'Утилизационный сбор: {yts}')
        print(f'Единая ставка: {duty}')
        print(f'Итого: {res_rus}')

        return round(toll)
    except Exception as e:
        print(f'Ошибка в calc_toll: {str(e)}')


def get_commissions(currency: Currency) -> tuple[float, float, float, float, float, float]:
    delivery = None 
    our_commission = None 
    broker = None
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
    url = 'http://127.0.0.1:8000/users/add-client/'  
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
            if response.status == 201:
                response_data = await response.json()
                print(f"Клиент успешно добавлен: {response_data['message']}, Client ID: {response_data['client_id']}")
            elif response.status == 400:
                response_data = await response.json()
                print(f"Ошибка: {response_data.get('error', 'Unknown error')}")
            else:
                print(f"Неизвестная ошибка: {response.status}")