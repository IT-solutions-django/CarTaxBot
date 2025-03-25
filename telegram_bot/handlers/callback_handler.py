import asyncio
from aiogram import types
from aiogram import F, Router
from settings.static import Message
from settings.utils import show_options
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from .state import CarDutyCalculation, ClientContacts
from settings.utils import (
    calc_toll, 
    set_contact_data, 
    format_float, 
    add_client_calculation,
)
from settings.static import EngineType, ClientType
from keyboards import keyboards
from enum import Enum

router = Router()


@router.callback_query(F.data == 'calculate_duty')
async def ask_currency(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CarDutyCalculation.car_type)
    car_type_buttons = keyboards.car_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=car_type_buttons)
    await callback.message.answer("Выберите тип автомобиля:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(CarDutyCalculation.car_type, F.data.startswith('car_type_'))
async def ask_currency(callback: types.CallbackQuery, state: FSMContext):
    car_type = callback.data.split('_')[-1]
    await state.update_data(car_type=car_type)
    await state.set_state(CarDutyCalculation.currency)
    currency_buttons = keyboards.currency_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=currency_buttons)
    await callback.message.answer("Выберите, в какой валюте будет указана цена автомобиля:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(CarDutyCalculation.currency, F.data.startswith('currency_'))
async def ask_cost(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split('_')[-1]
    await state.update_data(currency=currency)
    await state.set_state(CarDutyCalculation.cost)
    await callback.message.answer("Введите стоимость автомобиля (например, 1200000):")
    await callback.answer()


@router.message(CarDutyCalculation.cost, F.text.regexp(r'^\d+$'))
async def ask_engine_volume(message: types.Message, state: FSMContext):
    await state.update_data(cost=int(message.text))
    await state.set_state(CarDutyCalculation.engine_volume)
    await message.answer("Введите объём двигателя в см³ (например, 1500):")


@router.message(CarDutyCalculation.engine_volume, F.text.regexp(r'^\d+$'))
async def ask_engine_type(message: types.Message, state: FSMContext):
    await state.update_data(engine_volume=int(message.text))
    await state.set_state(CarDutyCalculation.engine_type)
    engine_type_buttons = keyboards.engine_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=engine_type_buttons)
    await message.answer("Выберите тип двигателя:", reply_markup=keyboard)


@router.callback_query(CarDutyCalculation.engine_type, F.data.startswith('engine_type_'))
async def ask_next_step(callback: types.CallbackQuery, state: FSMContext):
    engine_type = callback.data.split('_')[-1]
    await state.update_data(engine_type=engine_type)
    
    if engine_type in (EngineType.HYBRID_CONSISTENT.value, EngineType.ELECTRO.value):
        await state.set_state(CarDutyCalculation.power)
        await callback.message.answer("Введите 30-минутную мощность двигателя в кВт (например, 60):")
    else:
        await state.set_state(CarDutyCalculation.weight)
        await callback.message.answer("Введите массу автомобиля в тоннах (например, 1.5):")
    
    await callback.answer()


@router.message(CarDutyCalculation.power, F.text.regexp(r'^\d+$'))
async def ask_weight(message: types.Message, state: FSMContext):
    await state.update_data(power=int(message.text))
    await state.set_state(CarDutyCalculation.weight)
    await message.answer("Введите массу автомобиля в тоннах (например, 1.5):")

@router.message(CarDutyCalculation.weight, F.text.regexp(r'^\d+(\.\d+)?$'))
async def ask_client_type(message: types.Message, state: FSMContext):
    weight = float(message.text)
    await state.update_data(weight=weight)
    
    if weight > 5:
        await state.set_state(CarDutyCalculation.client_type)
        client_type_buttons = keyboards.client_type_buttons_only_physical
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=client_type_buttons)
        await message.answer("Кто ввозит автомобиль:", reply_markup=keyboard)
    else:
        await state.set_state(CarDutyCalculation.client_type)
        client_type_buttons = keyboards.client_type_buttons
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=client_type_buttons)
        await message.answer("Кто ввозит автомобиль:", reply_markup=keyboard)


@router.callback_query(CarDutyCalculation.client_type, F.data.startswith('client_type_'))
async def ask_age(callback: types.CallbackQuery, state: FSMContext):
    client_type = callback.data.split('_')[-1]
    await state.update_data(client_type=client_type)
    await state.set_state(CarDutyCalculation.age)
    age_buttons = keyboards.age_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=age_buttons)
    await callback.message.answer("Выберите возраст автомобиля:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(CarDutyCalculation.age, F.data.startswith('age_'))
async def calculate_duty(callback: types.CallbackQuery, state: FSMContext):
    age = callback.data.split('_')[-1]
    await state.update_data(age=age)
    data = await state.get_data()
    print(data)
    duty = calc_toll(
        price=data['cost'], 
        age=data['age'], 
        volume=data['engine_volume'], 
        currency=data['currency'], 
        engine_type=data['engine_type'], 
    )
    contacts_buttons = keyboards.contacts_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=contacts_buttons)
    await callback.message.answer(
        f"Стоимость: {format_float(data['cost'])} {data['currency']}\n"
        f"Объём двигателя: {data['engine_volume']} см³\n"
        f"Масса: {data['weight']} тонн\n"
        f"Возраст: {data['age']}\n"
        f"Тип двигателя: {data['engine_type']}\n"
        f"Размер пошлины: {format_float(duty)} рублей\n\n"
        f"Данный расчёт является приблизительным, свяжитесь с нами для уточнения деталей", 
        reply_markup=keyboard
    )

    await add_client_calculation(
        telegram_id=callback.from_user.id, 
        price=data['cost'], 
        age=data['age'], 
        engine_volume=data['engine_volume'], 
        currency=data['currency'], 
        engine_type=data['engine_type'], 
    )

    await state.clear()
    await callback.answer()


# Заявка

@router.callback_query(F.data == 'contact')
async def start_contact_collection(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ClientContacts.name)
    await callback.message.answer("Введите ваше имя (например, Максим):")
    await callback.answer()

@router.message(ClientContacts.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ClientContacts.phone)
    await message.answer("Введите ваш номер телефона (например, 71234567890 или 81234567890):")

@router.message(ClientContacts.phone, F.text.regexp(r'^(7|8)\d{10}$'))
async def process_phone_valid(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    contact_data = await state.get_data()
    
    await set_contact_data(
        telegram_id=message.from_user.id, 
        name=contact_data['name'], 
        phone=contact_data['phone']
    )
    
    await message.answer(
        "✅ Спасибо! Ваша заявка сохранена.\n"
        f"Имя: {contact_data['name']}\n"
        f"Телефон: {contact_data['phone']}\n\n"
        "Наш менеджер свяжется с вами в ближайшее время!"
    )
    await state.clear()

@router.message(ClientContacts.phone)
async def process_phone_invalid(message: types.Message):
    await message.answer("Пожалуйста, введите номер в правильном формате (например, 71234567890 или 81234567890)")