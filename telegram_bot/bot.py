from aiogram import Bot, Dispatcher
from dotenv import load_dotenv 
import asyncio
import os
from handlers import command_handler, callback_handler
from aiogram.client.default import DefaultBotProperties


load_dotenv()


API_TOKEN: str = os.getenv('API_TOKEN')
bot: Bot = Bot(
    token=API_TOKEN, 
    default=DefaultBotProperties(parse_mode='Markdown')
)
dp: Dispatcher = Dispatcher()


async def main() -> None:
    dp.include_router(callback_handler.router)
    dp.include_router(command_handler.router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())