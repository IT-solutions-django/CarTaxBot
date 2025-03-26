from aiogram import types
from settings.static import (
    EngineType, 
    ClientType,
    Currency,
    CarAge,
    CarType,
)


buttons_start = [
    [types.InlineKeyboardButton(text='Рассчитать пошлину', callback_data='calc')],
    [types.InlineKeyboardButton(text='Получить курсы валют', callback_data='currencies')],
    [types.InlineKeyboardButton(text='Оставить заявку', callback_data='feedback')],
]

feedback_button = [
   [types.InlineKeyboardButton(text='Оставить заявку', callback_data='feedback')],
]


client_type_buttons = [
    [types.InlineKeyboardButton(text=f'{client_type.value.capitalize()}', callback_data=f'client_type_{client_type.value}')] 
    for client_type in ClientType 
]

client_type_buttons_only_physical = [
    [types.InlineKeyboardButton(text=f'{client_type.value.capitalize()}', callback_data=f'client_type_{client_type.value}')] 
    for client_type in ClientType if client_type.value != 'юридическое лицо'
]

currency_buttons = [
    [types.InlineKeyboardButton(text='Юань', callback_data='currency_CNY')],
    [types.InlineKeyboardButton(text='Иена', callback_data='currency_JPY')],
    [types.InlineKeyboardButton(text='Вона', callback_data='currency_KRW')],
    [types.InlineKeyboardButton(text='Доллар', callback_data='currency_USD')],
    [types.InlineKeyboardButton(text='Евро', callback_data='currency_EUR')],
    [types.InlineKeyboardButton(text='Рубль', callback_data='currency_RUB')],
]

car_type_buttons = [
    [types.InlineKeyboardButton(text=f'{car_type.value.capitalize()}', callback_data=f'car_type_{car_type.value}')]
    for car_type in CarType if not car_type == CarType.CARGO
]

age_buttons = [
    [types.InlineKeyboardButton(text='Меньше 3-х лет', callback_data='age_less_3')],
    [types.InlineKeyboardButton(text='3-5 лет', callback_data='age_3_5')],
    [types.InlineKeyboardButton(text='5-7 лет', callback_data='age_5_7')],
    [types.InlineKeyboardButton(text='Больше 7 лет', callback_data='age_more_7')],
]


age_buttons = [
    [types.InlineKeyboardButton(text=f'{car_age.value.capitalize()}', callback_data=f'age_{car_age.value}')] 
    for car_age in CarAge
]

engine_type_buttons = [
    [types.InlineKeyboardButton(text=f'{engine_type.value.capitalize()}', callback_data=f'engine_type_{engine_type.value}')] 
    for engine_type in EngineType
]

contacts_buttons = [
    [types.InlineKeyboardButton(text="Позвонить: 7 (913) 795-65-56", callback_data='_')],
    [types.InlineKeyboardButton(text="Написать на почту", callback_data='_')]
]