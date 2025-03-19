from enum import Enum 


class Message(Enum): 
    START_MESSAGE: str = 'Этот бот предназначен для расчёта стоимости автомобиля при его растаможке'


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