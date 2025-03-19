from aiogram.filters import Command
from aiogram import types
from aiogram import Router
from settings.static import Message
from keyboards.keyboards import buttons_start
from settings.utils import show_options


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_start)
    await message.answer(Message.START_MESSAGE, reply_markup=keyboard)


@router.message(Command("calculate_duty"))
async def command_get_company_info(message: types.Message) -> None:
    await show_options(message, {'словарь': 'словарик'}, 'ыыы', 'info')

