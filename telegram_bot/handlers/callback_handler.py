import asyncio
from aiogram import types
from aiogram import F, Router
from settings.static import Message
from settings.utils import show_options
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from .state import CarDutyCalculation, ClientContacts
from settings.utils import calc_toll, set_contact_data

from keyboards import keyboards

router = Router()


@router.callback_query(F.data == 'calculate_duty')
async def ask_currency(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CarDutyCalculation.currency)
    
    currency_buttons = keyboards.currency_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=currency_buttons)
    await callback.message.answer("Выберите валюту стоимости:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(CarDutyCalculation.currency, F.data.startswith('currency_'))
async def ask_cost(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split('_')[-1]
    await state.update_data(currency=currency)
    await state.set_state(CarDutyCalculation.cost)

    await callback.message.answer("Введите стоимость автомобиля:")
    await callback.answer()


@router.message(CarDutyCalculation.cost, F.text.regexp(r'^\d+$'))
async def ask_engine_volume(message: types.Message, state: FSMContext):
    await state.update_data(cost=int(message.text))
    await state.set_state(CarDutyCalculation.engine_volume)
    await message.answer("Введите объём двигателя (в см³):")


@router.message(CarDutyCalculation.engine_volume, F.text.regexp(r'^\d+$'))
async def ask_power(message: types.Message, state: FSMContext):
    await state.update_data(engine_volume=int(message.text))
    await state.set_state(CarDutyCalculation.power)

    await message.answer("Введите мощность двигателя (в л.с. или кВт):")


@router.message(CarDutyCalculation.power, F.text.regexp(r'^\d+$'))
async def ask_weight(message: types.Message, state: FSMContext):
    await state.update_data(power=int(message.text))
    await state.set_state(CarDutyCalculation.weight)

    await message.answer("Введите массу автомобиля (в тоннах):")


@router.message(CarDutyCalculation.weight, F.text.regexp(r'^\d+(\.\d+)?$'))
async def ask_age(message: types.Message, state: FSMContext):
    await state.update_data(weight=float(message.text))
    await state.set_state(CarDutyCalculation.age)

    age_buttons = keyboards.age_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=age_buttons)
    await message.answer("Выберите возраст автомобиля:", reply_markup=keyboard)


@router.callback_query(CarDutyCalculation.age, F.data.startswith('age_'))
async def ask_engine_type(callback: types.CallbackQuery, state: FSMContext):
    age = callback.data.split('_')[-1]
    await state.update_data(age=age)
    await state.set_state(CarDutyCalculation.engine_type)

    engine_type_buttons = keyboards.engine_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=engine_type_buttons)
    await callback.message.answer("Выберите тип двигателя:", reply_markup=keyboard)
    await callback.answer()


# Шаг 8: Расчёт пошлины и вывод результата
@router.callback_query(CarDutyCalculation.engine_type, F.data.startswith('engine_type_'))
async def calculate_duty(callback: types.CallbackQuery, state: FSMContext):
    engine_type = callback.data.split('_')[-1]
    await state.update_data(engine_type=engine_type)

    data = await state.get_data()
    
    cost = data['cost']
    engine_volume = data['engine_volume']
    currency = data['currency']
    power = data['power']
    weight = data['weight']
    age = data['age']
    engine_type = data['engine_type']

    duty = calc_toll(
        price=cost, 
        age=age, 
        volume=engine_volume, 
        currency=currency, 
        engine_type=engine_type, 
    )

    await callback.message.answer(
        f"Стоимость: {cost} {currency}\n"
        f"Объём двигателя: {engine_volume} см³\n"
        f"Мощность: {power} л.с./кВт\n"
        f"Масса: {weight} тонн\n"
        f"Возраст: {age}\n"
        f"Тип двигателя: {engine_type}\n"
        f"Размер пошлины: {duty} рублей\n\n"
        f"Данный расчёт является приблизительным, свяжитесь с нами для уточнения деталей"
    )

    await state.clear()  
    await callback.answer()




@router.callback_query(F.data == 'contact')
async def ask_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ClientContacts.name)
    await callback.message.answer("Введите ваше имя:")
    await callback.answer()


@router.message(ClientContacts.name, F.text.regexp(r'^[a-zA-Zа-яА-ЯёЁ\s]+$'))
async def ask_phone(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ClientContacts.phone)

    await message.answer("Введите ваш номер телефона (например: +7 123 456 67-89):")


@router.message(ClientContacts.phone, F.text.regexp(r'.*'))
async def confirm_info(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    data = await state.get_data()
    name = data['name']
    phone = data['phone']

    await message.answer(
        f"Ваши данные:\n"
        f"- Имя: {name}\n"
        f"- Телефон: {phone}\n\n"
        f"Спасибо! Мы скоро с вами свяжемся"
    )

    await state.clear()

    await set_contact_data(
        telegram_id=message.from_user.id, 
        name=name, 
        phone=phone
    ) 