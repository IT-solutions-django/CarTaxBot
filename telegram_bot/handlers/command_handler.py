from aiogram.filters import Command
from aiogram import types
from aiogram import Router
from settings.static import Message
from keyboards.keyboards import buttons_start
from settings.utils import show_options, add_new_client


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_start)

    await message.answer(Message.START_MESSAGE, reply_markup=keyboard)

    await add_new_client(
        telegram_id=message.from_user.id
    )



# Только для тестов
