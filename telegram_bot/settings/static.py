from enum import Enum 


class Message(Enum): 
    START_MESSAGE: str = (
        "Вас приветствует бот-калькулятор компании ООО «Автотерминал», который поможет рассчитать стоимость таможенных платежей и утилизационного сбора.\n\n"
        "Для использования бота, а также, чтобы быть в курсе событий в автомобильной среде и изменений таможенного законодательства подпишитесь на [наш телеграмм-канал](https://t.me/avterminaal)"
    )
    CONTACT_MESSAGE: str = (
        "Остались вопросы? Хотите оставить заявку?\n"
        "Свяжитесь с нами!\n\n"
        "Контакты нашей компании:\n"
        "🤙+7(804)7005188\n"
        "📲 +79084463450 (WA) \n"
        "📧 av.terminal@mail.ru\n"
        "🌐 avterminal.ru\n"
        "💬 https://t.me/avterminaal"
    )


class BackendURL(Enum):
    PROD_DOMAIN: str = 'backend' 
    DEV_DOMAIN: str = '127.0.0.1' 

    ADD_CLIENT: str = 'users/add-client/' 
    SET_CONTACT_DATA: str = 'users/leave-request/'
    ADD_CLIENT_CALCULATION: str = 'users/add-calculation/'

    GET_EXCHANGE_RATES: str = 'http://193.164.149.51/currencies/get-exchange-rates-from-cbr/'

    DOMAIN = PROD_DOMAIN


class Currency(Enum): 
    JPY: str = 'JPY'
    KRW: str = 'KRW' 
    CNY: str = 'CNY'
    EUR: str = 'EUR' 
    USD: str = 'USD' 
    RUB: str = 'RUB'


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


class CarType(Enum): 
    PASSENGER = 'легковой' 
    SNOWMOBILE = 'снегоход' 
    QUAD_BIKE = 'квадроцикл'
    CARGO = 'грузовое'