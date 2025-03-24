from enum import Enum 


class Message(Enum): 
    START_MESSAGE: str = 'Этот бот предназначен для расчёта стоимости автомобиля при его растаможке'


class BackendURL(Enum):
    PROD_DOMAIN: str = 'backend' 
    DEV_DOMAIN: str = '127.0.0.1' 
    DOMAIN = DEV_DOMAIN
    ADD_CLIENT: str = 'users/add-client/' 
    SET_CONTACT_DATA: str = 'users/set-contact-data/'


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
    HYBRID: str = 'гибрид'