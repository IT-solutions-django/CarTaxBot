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
from settings.static import EngineType, ClientType, CarType, Currency
from keyboards import keyboards
from settings.utils import get_exchange_rates
from datetime import datetime

router = Router()


# Курсы валют

@router.callback_query(F.data == 'currencies')
async def ask_currency(callback: types.CallbackQuery):
    exchange_rates: dict[dict] = await get_exchange_rates() 

    text = '📈 Актуальные курсы валют:\n\n'
    all_dates = []
    for currency_name, currency_data in exchange_rates.items(): 
        text += f"{currency_name} - {currency_data['exchange_rate']} ₽\n"
        updated_at: datetime = datetime.strptime(currency_data['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        all_dates.append(updated_at.date())

    if all(d == all_dates[0] for d in all_dates):
        common_date = all_dates[0].strftime('%d.%m.%Y')
        text += f"\n✅ Все данные актуальны на {common_date}\nИсточник - Центральный банк РФ"

    await callback.message.answer(text)
    await callback.answer()


# Расчёт пошлины

@router.callback_query(F.data == 'calc')
async def ask_currency(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CarDutyCalculation.car_type)
    car_type_buttons = keyboards.car_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=car_type_buttons)
    await callback.message.answer("Выберите тип автомобиля:", reply_markup=keyboard)
    await callback.answer()


# Тип автомобиля
@router.callback_query(CarDutyCalculation.car_type, F.data.startswith('car_type_'))
async def ask_currency(callback: types.CallbackQuery, state: FSMContext):
    car_type = callback.data.split('_')[-1]
    await state.update_data(car_type=car_type)
    await state.set_state(CarDutyCalculation.currency)
    currency_buttons = keyboards.currency_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=currency_buttons)
    await callback.message.answer("Выберите, в какой валюте будет указана цена автомобиля:", reply_markup=keyboard)
    await callback.answer()


# Валюта
@router.callback_query(CarDutyCalculation.currency, F.data.startswith('currency_'))
async def ask_cost(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split('_')[-1]
    await state.update_data(currency=currency)
    await state.set_state(CarDutyCalculation.cost)
    await callback.message.answer("Введите стоимость автомобиля (например, 1200000):")
    await callback.answer()


# Стоимость
@router.message(CarDutyCalculation.cost, F.text.regexp(r'^\d+$'))
async def ask_engine_volume(message: types.Message, state: FSMContext):
    await state.update_data(cost=int(message.text))
    await state.set_state(CarDutyCalculation.engine_volume)
    await message.answer("Введите объём двигателя в см³ (например, 1500):")


# Объём двигателя
@router.message(CarDutyCalculation.engine_volume, F.text.regexp(r'^\d+$'))
async def ask_engine_type(message: types.Message, state: FSMContext):
    await state.update_data(engine_volume=int(message.text))
    await state.set_state(CarDutyCalculation.engine_type)
    engine_type_buttons = keyboards.engine_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=engine_type_buttons)
    await message.answer("Выберите тип двигателя:", reply_markup=keyboard)


# Тип двигателя
@router.callback_query(CarDutyCalculation.engine_type, F.data.startswith('engine_type_'))
async def ask_next_step(callback: types.CallbackQuery, state: FSMContext):
    engine_type = callback.data.split('_')[-1]
    await state.update_data(engine_type=engine_type)

    # Сначала спрашиваем, кто ввозит авто
    await state.set_state(CarDutyCalculation.client_type)
    client_type_buttons = keyboards.client_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=client_type_buttons)
    await callback.message.answer("Кто ввозит автомобиль:", reply_markup=keyboard)
    await callback.answer()


# Кто ввозит
@router.callback_query(CarDutyCalculation.client_type, F.data.startswith('client_type_'))
async def ask_age(callback: types.CallbackQuery, state: FSMContext):
    print('klfjsenr')
    client_type = callback.data.split('_')[-1]
    await state.update_data(client_type=client_type)

    if client_type == ClientType.PHYSICAL.value: 
        data = await state.get_data() 
        if data['engine_type'] in (EngineType.ELECTRO.value, EngineType.HYBRID_CONSISTENT.value):
            await state.set_state(CarDutyCalculation.power)
            await callback.message.answer('Введите 30-минутную мощность автомобиля в кВт:')
            await callback.answer()
        else:
            await state.set_state(CarDutyCalculation.age)
            age_buttons = keyboards.age_buttons
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=age_buttons)
            await callback.message.answer("Введите возраст автомобиля:", reply_markup=keyboard)
            await callback.answer()
    elif client_type == ClientType.JURIDICAL.value: 
        await state.set_state(CarDutyCalculation.power)
        text = ''
        data = await state.get_data() 
        if data['engine_type'] in (EngineType.ELECTRO.value, EngineType.HYBRID_CONSISTENT.value):
            text = ("Введите 30-минутную мощность автомобиля в кВт:")
        else: 
            text = ("Введите мощность автомобиля в л. с.:")

        await callback.message.answer(text)
        await callback.answer()


# Этот шаг (Мощность) только для электромобилей и последовательных гибридов
@router.message(CarDutyCalculation.power, F.text.regexp(r'^\d+$'))
async def ask_weight(message: types.Message, state: FSMContext):
    await state.update_data(power=int(message.text))
    data = await state.get_data() 
    car_type = data.get('car_type')

    await state.set_state(CarDutyCalculation.age)
    age_buttons = keyboards.age_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=age_buttons)
    await message.answer("Выберите возраст автомобиля:", reply_markup=keyboard)


# Возраст
@router.callback_query(CarDutyCalculation.age, F.data.startswith('age_'))
async def calculate_duty(callback: types.CallbackQuery, state: FSMContext):
    age = callback.data.split('_')[-1]
    await state.update_data(age=age)
    data = await state.get_data()
    power_kw = data.get('power')
    if data['engine_type'] not in (EngineType.ELECTRO.value, EngineType.HYBRID_CONSISTENT.value): 
        if power_kw:
            power_kw = power_kw * 0.75
    duty_data = await calc_toll(
        price=data['cost'], 
        age=data['age'], 
        volume=data['engine_volume'], 
        currency=data['currency'], 
        car_type=data['car_type'],
        client_type=data['client_type'],
        power_kw=power_kw,
        engine_type=data['engine_type'], 
    )
    message_text = (
        f"Тип: {data['car_type']}\n"
        f"Стоимость: {format_float(data['cost'])} {data['currency']}\n"
        f"Объём двигателя: {data['engine_volume']} см³\n"
    )

    if 'weight' in data and data['weight']:
        message_text += f"Масса: {data['weight']} тонн\n"

    message_text += (
        f"Возраст: {data['age']}\n"
        f"Тип двигателя: {data['engine_type']}\n"
    ) 
    print(duty_data)
    duty, yts, tof, commission, nds, excise, result, exchange_rates = (
        duty_data.get('duty'),
        duty_data.get('yts'),
        duty_data.get('tof'),
        duty_data.get('commission'),
        duty_data.get('nds'),
        duty_data.get('excise'),
        duty_data.get('result'), 
        duty_data.get('exchange_rates'),
    )
    message_text += (
        f"\n*Результаты расчёта*:\n"
        f"Таможенная пошлина: {format_float(duty)} ₽\n"
        f"Утилизационный сбор: {format_float(yts)} ₽\n"
        f"Таможенные сборы: {format_float(tof)} ₽\n"
    )
    if nds: 
        message_text += f"НДС: {format_float(nds)} ₽\n"
    if excise: 
        message_text += f"Акциз: {format_float(excise)} ₽\n"
    message_text += f"Комиссия компании: {format_float(commission)} ₽\n\n"
    if data['currency'] != Currency.RUB.value: 
        currency = data['currency']
        updated_at = datetime.strptime(exchange_rates[currency]['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        message_text += f"Курс на {updated_at.strftime('%d.%m.%Y')}: 1 {currency} = {exchange_rates[currency]['exchange_rate']} ₽\n\n"
    message_text += (
        f"*Итоговая сумма: {format_float(result)} ₽*\n\n"
        "Данный расчёт является приблизительным, свяжитесь с нами для уточнения деталей\n\n"
        "*Телефон: +7 (111) 111-11-11*\n"
        "*Email: example@example.com*\n\n"
        "Также Вы можете оставить заявку и наш менеджер свяжется с Вами в ближайшее время"
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboards.feedback_button)
    await callback.message.answer(message_text, reply_markup=keyboard)
    await callback.answer()

    # await add_client_calculation(
    #     telegram_id=callback.from_user.id, 
    #     price=data['cost'], 
    #     age=data['age'], 
    #     engine_volume=data['engine_volume'], 
    #     currency=data['currency'], 
    #     engine_type=data['engine_type'], 
    #     car_type=data['car_type'], 
    #     power_kw=data.get('power')
    # )

    await state.clear()


# Заявка

@router.callback_query(F.data == 'feedback')
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



# Получить курсы валют