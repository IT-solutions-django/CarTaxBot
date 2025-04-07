from aiogram.filters import Command
from aiogram import types
from aiogram import Router
from settings.static import Message
from keyboards.keyboards import buttons_start
from settings.utils import add_new_client
from aiogram.fsm.context import FSMContext
from keyboards import keyboards
from .state import CarDutyCalculation, ClientContacts
from .state import ClientContacts
from datetime import datetime


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_start)

    await message.answer(Message.START_MESSAGE, reply_markup=keyboard, disable_web_page_preview=True)

    await add_new_client(
        telegram_id=message.from_user.id, 
        telegram_username=message.from_user.username
    )


@router.message(Command("feedback"))
async def send_welcome(message: types.Message, state=FSMContext) -> None:
    await state.set_state(ClientContacts.name)
    await message.answer("Введите ваше имя (например, Максим):")


@router.message(Command("calc"))
async def send_welcome(message: types.Message, state=FSMContext) -> None:
    await state.set_state(CarDutyCalculation.car_type)
    car_type_buttons = keyboards.car_type_buttons
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=car_type_buttons)
    await message.answer("Выберите тип автомобиля:", reply_markup=keyboard)


@router.message(Command('currency'))
async def start_contact_collection(message: types.Message):
    from bot import get_rates
    exchange_rates: dict = await get_rates()

    text = '📈 Актуальные курсы валют:\n\n'
    all_dates = []
    for currency_name, currency_data in exchange_rates.items(): 
        text += f"{currency_name} - {currency_data['exchange_rate']} ₽\n"
        updated_at: datetime = datetime.strptime(currency_data['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        all_dates.append(updated_at.date())

    if all(d == all_dates[0] for d in all_dates):
        common_date = all_dates[0].strftime('%d.%m.%Y')
        text += f"\n✅ Все данные актуальны на {common_date}\nИсточник - Центральный банк РФ"

    await message.answer(text)