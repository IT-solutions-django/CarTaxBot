from aiogram.filters import Command
from aiogram import types
from aiogram import Router
from settings.static import Message
from keyboards.keyboards import buttons_start, contacts_buttons
from settings.utils import show_options, add_new_client
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .state import ClientContacts


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_start)

    await message.answer(Message.START_MESSAGE, reply_markup=keyboard)

    await add_new_client(
        telegram_id=message.from_user.id
    )


@router.message(Command("contact"))
async def send_welcome(message: types.Message, state=FSMContext) -> None:
    await state.set_state(ClientContacts.name)
    await message.answer("Введите ваше имя (например, Максим):")


@router.message(Command("about"))
async def send_welcome(message: types.Message, state=FSMContext) -> None:
    await message.answer(
        f"Информация о компании\n\n"
        f"текст\n"
        f"текст\n"
        f"текст\n\n"
        f"Телефон: +7 (111) 111-11-11\n"
        f"Email: example@example.com"
    )
