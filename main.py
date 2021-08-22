import asyncio
import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from utils.commands import set_commands
from utils.config import BOT_TOKEN

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, loop=loop, storage=storage)
logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    await set_commands(dispatcher)


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
