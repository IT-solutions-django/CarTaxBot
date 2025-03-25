from enum import Enum 


class Message(Enum): 
    START_MESSAGE: str = (
        "🚗 *Бот для расчёта растаможки автомобиля*\n\n"
        "Рассчитайте примерную стоимость таможенных платежей для вашего авто. "
        "Просто введите параметры или воспользуйтесь кнопками ниже."
    )
    CONTACT_MESSAGE: str = (
        "📞 *Свяжитесь с нами!*\n\n"
        "• Телефон: +7 (123) 456-78-90\n"
        "• Почта: customs@example.com\n"
        "• Работаем: Пн-Пт, 9:00–18:00"
    )


class BackendURL(Enum):
    PROD_DOMAIN: str = 'backend' 
    DEV_DOMAIN: str = '127.0.0.1' 

    ADD_CLIENT: str = 'users/add-client/' 
    SET_CONTACT_DATA: str = 'users/leave-request/'
    ADD_CLIENT_CALCULATION: str = 'users/add-calculation/'

    DOMAIN = DEV_DOMAIN


class Currency(Enum): 
    JPY: str = 'JPY'
    KRW: str = 'KRW' 
    CNY: str = 'CNY'
    EUR: str = 'EUR' 
    USD: str = 'USD' 


class EngineType(Enum): 
    PETROL: str = 'бензин' 
    DIESEL: str = 'дизель' 
    ELECTRO: str = 'электро' 
    HYBRID_PARALLEL: str = 'гибрид параллельный'
    HYBRID_CONSISTENT: str = 'гибрид последовательный'


class ClientType(Enum):
    PHYSICAL = 'физическое лицо' 
    JURIDICAL = 'юридическое лицо'


class CarAge(Enum): 
    LESS_THAN_3 = 'меньше 3-х лет' 
    FROM_3_TO_5 = '3-5 лет'
    FROM_5_TO_7 = '5-7 лет' 
    MORE_THAN_7 = 'больше 7 лет'


class ContactData(Enum): 
    PHONE = '+7 (111) 111-11-11'