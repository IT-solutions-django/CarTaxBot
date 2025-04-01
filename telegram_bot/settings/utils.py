from settings.static import Currency, EngineType
import aiohttp
import json
from settings.static import (
    Currency, 
    CarAge, 
    CarType,
    ClientType,
)
from settings.static import BackendURL


back_domain = BackendURL.DOMAIN.value



async def calc_toll(price: int, age: str, volume: int, currency: str, car_type: str, client_type: str, power_kw: float = None, engine_type: str = None) -> dict:
    """
    duty - пошлина
    tof - таможенное оформление
    yts - утилизационный сбор
    nds - НДС 
    excise - акциз
    """
    try:
        currency: Currency = Currency(currency)
        engine_type = EngineType(engine_type)
        age: CarAge = CarAge(age)
        car_type: CarType = CarType(car_type)
        client_type: ClientType = ClientType(client_type)

        from bot import get_rates
        exchange_rates = await get_rates()

        price = float(price)
        volume = int(volume)
        nds = None
        excise = None
        duty = None

        # Перевод цены в рубли
        if currency == Currency.RUB:
            one_rub = 1
        else:
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

        if car_type == CarType.PASSENGER or car_type == CarType.CARGO:
            if age == CarAge.LESS_THAN_3:
                # Утилизационный сбор (физ и юр)
                if volume > 3500:
                    yts = 20000*137.11 
                elif (volume > 3000) and (volume <= 3499):
                    yts = 20000*107.67 
                elif (volume > 2000) and (volume <= 3000):
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.17 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*93.77
                elif (volume > 1000) and (volume <= 2000):
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.17 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*33.37
                else:
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.17 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*9.01
                europrice = price_rus / exchange_rates['EUR']['exchange_rate']

                # Пошлина (физ)
                if client_type == ClientType.PHYSICAL:
                    if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
                        duty = europrice * 0.15
                        yts = 20000*0.17 
                    elif europrice < 8500:
                        duty = europrice * 0.54
                        if duty / volume < 2.5:
                            duty = volume * 2.5
                    elif (europrice > 8500) and (europrice <= 16700):
                        duty = europrice * 0.48 
                        if duty / volume < 3.5:
                            duty = volume * 3.5
                    elif (europrice > 16700) and (europrice <= 42300):
                        duty = europrice * 0.48
                        if duty / volume < 5.5:
                            duty = volume * 5.5
                    elif (europrice > 42300) and (europrice <= 84500):
                        duty = europrice * 0.48
                        if duty / volume < 7.5:
                            duty = volume * 7.5
                    elif (europrice > 84500) and (europrice <= 169000):
                        duty = europrice * 0.48
                        if duty / volume < 15:
                            duty = volume * 15
                    else:
                        duty = europrice * 0.48
                        if duty / volume < 20:
                            duty = volume * 20
                # Пошлина (юр)
                elif client_type == ClientType.JURIDICAL: 
                    if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
                        duty = europrice * 0.15
                        yts = 20000*33.37  
                    elif engine_type in (EngineType.PETROL,): 
                        if volume <= 1000:
                            duty = europrice * 0.15
                        elif (volume >= 1001) and (volume <= 1500):
                            duty = europrice * 0.15
                        elif (volume >= 1501) and (volume <= 1800):
                            duty = europrice * 0.15
                        elif (volume >= 1801) and (volume <= 2300):
                            duty = europrice * 0.15
                        elif (volume >= 2301) and (volume <= 3000):
                            duty = europrice * 0.15
                        else:
                            duty = europrice * 0.125
                    elif engine_type == EngineType.DIESEL: 
                        if volume <= 1500:
                            duty = europrice * 0.15
                        elif (volume >= 1501) and (volume <= 2500):
                            duty = europrice * 0.15
                        else:
                            duty = europrice * 0.15
            
            elif age == CarAge.FROM_3_TO_5:
                # Утилизационный сбор (физ и юр)
                if volume > 3500:
                    yts = 20000*180.24 
                elif (volume > 3000) and (volume <= 3500):
                    yts = 20000*164.84 
                elif (volume > 2000) and (volume <= 3000):
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.26 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*141.97
                elif (volume > 1000) and (volume <= 2000):
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.26 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*58.7
                else:
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.26 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*23
                
                if client_type == ClientType.PHYSICAL:
                    europrice = price_rus / exchange_rates['EUR']['exchange_rate']
                    if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
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
                elif client_type == ClientType.JURIDICAL:
                    europrice = price_rus / exchange_rates['EUR']['exchange_rate']
                    if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
                        duty = europrice * 0.15
                        yts = 20000*58.7
                    elif engine_type in (EngineType.PETROL,):
                        if volume <= 1000:
                            duty = europrice * 0.20 
                            if duty / volume < 0.36: 
                                duty = volume * 0.36
                        elif (volume >= 1001) and (volume <= 1500):
                            duty = europrice * 0.20
                            if duty / volume < 0.4: 
                                duty = volume * 0.4
                        elif (volume >= 1501) and (volume <= 1800):
                            duty = europrice * 0.20
                            if duty / volume < 0.36: 
                                duty = volume * 0.36
                        elif (volume >= 1801) and (volume <= 2300):
                            duty = europrice * 0.20
                            if duty / volume < 0.44: 
                                duty = volume * 0.44
                        elif (volume >= 2301) and (volume <= 3000):
                            duty = europrice * 0.20
                            if duty / volume < 0.44: 
                                duty = volume * 0.44
                        else:
                            duty = europrice * 0.20
                            if duty / volume < 0.8: 
                                duty = volume * 0.8
                    elif engine_type == EngineType.DIESEL:
                        if volume <= 1500:
                            duty = europrice * 0.20
                            if duty / volume < 0.32: 
                                duty = volume * 0.32
                        elif (volume >= 1501) and (volume <= 2500):
                            duty = europrice * 0.20
                            if duty / volume < 0.32: 
                                duty = volume * 0.4
                        else:
                            duty = europrice * 0.20
                            if duty / volume < 0.32: 
                                duty = volume * 0.8

            elif age == CarAge.FROM_5_TO_7 or age == CarAge.MORE_THAN_7:
                if volume > 3500:
                    yts = 20000*180.24 
                elif (volume > 3000) and (volume <= 3500):
                    yts = 20000*164.84 
                elif (volume > 2000) and (volume <= 3000):
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.26 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*141.97
                elif (volume > 1000) and (volume <= 2000):
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.26 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*58.7
                else:
                    if client_type == ClientType.PHYSICAL: 
                        yts = 20000*0.26 
                    elif client_type == ClientType.JURIDICAL: 
                        yts = 20000*23

                europrice = price_rus / exchange_rates['EUR']['exchange_rate']
                if client_type == ClientType.PHYSICAL:
                    if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
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
                elif client_type == ClientType.JURIDICAL: 
                    if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
                        duty = europrice * 0.15
                        yts = 20000*58.7
                    elif engine_type in (EngineType.PETROL,): 
                        if age == CarAge.FROM_5_TO_7:
                            if volume <= 1000:
                                duty = europrice * 0.20 
                                if duty / volume < 0.36: 
                                    duty = volume * 0.36
                            elif (volume >= 1001) and (volume <= 1500):
                                duty = europrice * 0.20
                                if duty / volume < 0.4: 
                                    duty = volume * 0.4
                            elif (volume >= 1501) and (volume <= 1800):
                                duty = europrice * 0.20
                                if duty / volume < 0.36: 
                                    duty = volume * 0.36
                            elif (volume >= 1801) and (volume <= 2300):
                                duty = europrice * 0.20
                                if duty / volume < 0.44: 
                                    duty = volume * 0.44
                            elif (volume >= 2301) and (volume <= 3000):
                                duty = europrice * 0.20
                                if duty / volume < 0.44: 
                                    duty = volume * 0.44
                            else:
                                duty = europrice * 0.20
                                if duty / volume < 0.8: 
                                    duty = volume * 0.8
                        elif age == CarAge.MORE_THAN_7: 
                            if volume <= 1000:
                                duty = volume * 1.4
                            elif (volume >= 1001) and (volume <= 1500):
                                duty = volume * 1.5
                            elif (volume >= 1501) and (volume <= 1800):
                                duty = volume * 1.6
                            elif (volume >= 1801) and (volume <= 2300):
                                duty = volume * 2.2
                            elif (volume >= 2301) and (volume <= 3000):
                                duty = volume * 2.2
                            else:
                                duty = volume * 3.2
                    elif engine_type == EngineType.DIESEL: 
                        if age == CarAge.FROM_5_TO_7: 
                            if volume <= 1500:
                                duty = europrice * 0.20
                                if duty / volume < 0.32: 
                                    duty = volume * 0.32
                            elif (volume >= 1501) and (volume <= 2500):
                                duty = europrice * 0.20
                                if duty / volume < 0.32: 
                                    duty = volume * 0.4
                            else:
                                duty = europrice * 0.20
                                if duty / volume < 0.32: 
                                    duty = volume * 0.8
                        elif age == CarAge.MORE_THAN_7: 
                            if volume <= 1500:
                                duty = volume * 1.5
                            elif (volume >= 1501) and (volume <= 2500):
                                duty = volume * 2.2
                            else:
                                duty = volume * 3.2

            # Акциз (готово)
            if client_type == ClientType.JURIDICAL: 
                if power_kw <= 67.5:
                    excise = 0
                elif power_kw <= 112.5:
                    excise = (power_kw / 0.75) * 61
                elif power_kw <= 150:
                    excise = (power_kw / 0.75) * 583
                elif power_kw <= 225:
                    excise = (power_kw / 0.75) * 955
                elif power_kw <= 300:
                    excise = (power_kw / 0.75) * 1628
                elif power_kw <= 375:
                    excise = (power_kw / 0.75) * 1685
                else:
                    excise = (power_kw / 0.75) * 1740 

            if client_type == ClientType.PHYSICAL:
                if engine_type in (EngineType.ELECTRO, EngineType.HYBRID_CONSISTENT):
                    duty = price_rus * 0.15
                    nds_percent = 0.2

                    if power_kw is not None:
                        if power_kw <= 67.5:
                            excise = 0
                        elif power_kw <= 112.5:
                            excise = (power_kw / 0.75) * 61
                        elif power_kw <= 150:
                            excise = (power_kw / 0.75) * 583
                        elif power_kw <= 225:
                            excise = (power_kw / 0.75) * 955
                        elif power_kw <= 300:
                            excise = (power_kw / 0.75) * 1628
                        elif power_kw <= 375:
                            excise = (power_kw / 0.75) * 1685
                        else:
                            excise = (power_kw / 0.75) * 1740 
                    else: 
                        raise Exception('Для электромобиля не указана мощность')

                    nds = (price_rus + duty + excise) * nds_percent
                    toll = duty + tof + yts + nds + excise
                else:
                    duty = duty * exchange_rates['EUR']['exchange_rate']
                    toll = duty + tof + yts

                result = toll
            elif client_type == ClientType.JURIDICAL: 
                nds_percent = 0.2
                duty = duty * exchange_rates['EUR']['exchange_rate']
                
                nds = (price_rus + duty + excise) * nds_percent
                toll = duty + tof + yts + nds + excise
                result = toll

            print(f'Таможенное оформление: {tof}')
            print(f'Утилизационный сбор: {yts}')
            print(f'Единая ставка: {duty}')
            print(f'Итого: {result}') 
        
        elif car_type in (CarType.QUAD_BIKE, CarType.SNOWMOBILE): 
            duty_percent = 0.05 
            nds_percent = 0.2 
            yts = 120750 

            duty = price_rus * duty_percent 
            nds = (price_rus + duty) * nds_percent 

            result = duty + nds + yts + tof

        result += 69000
        return {
            'tof': tof, 
            'yts': yts, 
            'duty': duty, 
            'commission': 69000,
            'result': result, 
            'nds': nds, 
            'excise': excise, 
            'exchange_rates': exchange_rates
        }

        
    except Exception as e:
        print(f'Ошибка в calc_toll: {str(e)}')


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


async def add_new_client(telegram_id: int, telegram_username: str = None, name: str = None, phone: str = None) -> None:
    url = f'http://{back_domain}:8000/users/add-client/'  
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'telegram_id': telegram_id,
        'telegram_username': telegram_username,
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
    telegram_id: int, 
    age: str, 
    engine_volume: float, 
    currency: str, 
    engine_type: str, 
    car_type: str, 
    result: str,
    power_kw: float = None
) -> None:
    url = f'http://{back_domain}:8000/{BackendURL.ADD_CLIENT_CALCULATION.value}'  
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'telegram_id': telegram_id,
        'age': age,
        'engine_volume': engine_volume,
        'currency': currency,
        'engine_type': engine_type,
        'car_type': car_type, 
        'power_kw': power_kw, 
        'result': result,
    }

    print(data)

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
    result = f"{round(number, 2):_}".replace("_", " ")
    return result