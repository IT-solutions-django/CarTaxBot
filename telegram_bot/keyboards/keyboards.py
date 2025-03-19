from aiogram import types
from settings.static import EngineType


buttons_start = [
    [types.InlineKeyboardButton(text='Расчёт пошлины', callback_data='calculate_duty')],
    [types.InlineKeyboardButton(text='О компании', callback_data='about_company')],
    [types.InlineKeyboardButton(text='Связаться', callback_data='contact')],
]

currency_buttons = [
    [types.InlineKeyboardButton(text='Доллар', callback_data='currency_USD')],
    [types.InlineKeyboardButton(text='Евро', callback_data='currency_EUR')],
    [types.InlineKeyboardButton(text='Юань', callback_data='currency_CNY')],
    [types.InlineKeyboardButton(text='Вона', callback_data='currency_KRW')],
    [types.InlineKeyboardButton(text='Иена', callback_data='currency_JPY')],
]

car_type_buttons = [
    [types.InlineKeyboardButton(text='Легковой', callback_data='car_type_легковой')],
    [types.InlineKeyboardButton(text='Снегоход', callback_data='car_type_снегоход')],
    [types.InlineKeyboardButton(text='Квадроцикл', callback_data='car_type_квадроцикл')],
]

age_buttons = [
    [types.InlineKeyboardButton(text='Меньше 3-х лет', callback_data='age_less_3')],
    [types.InlineKeyboardButton(text='3-5 лет', callback_data='age_3_5')],
    [types.InlineKeyboardButton(text='5-7 лет', callback_data='age_5_7')],
    [types.InlineKeyboardButton(text='Больше 7 лет', callback_data='age_more_7')],
]

engine_type_buttons = [
    [types.InlineKeyboardButton(text=f'{engine_type.value.capitalize()}', callback_data=f'engine_type_{engine_type.value}')] for engine_type in EngineType
]