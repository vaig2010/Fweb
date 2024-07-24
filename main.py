import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.handlers import router
from app.database.models import async_main

from dotenv import load_dotenv

from background import keep_alive

import pip


pip.main(['install', 'aiogram'])
pip.main(['install', 'flask'])
pip.main(['install', 'asyncio'])
pip.main(['install', 'aiosqlite'])
pip.main(['install', 'python-dotenv'])

pip.main(['install', 'sqlalchemy[asyncio]'])

# Разрешенные типы обновлений, которые будут обрабатываться ботом
ALLOWED_UPDATES = [
    "message", "edited_message", "inline_query", "chosen_inline_result",
    "callback_query"
]


async def main():
    await async_main()
    load_dotenv()
    telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
    bot = Bot(telegram_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


keep_alive()
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
