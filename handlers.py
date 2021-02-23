from main import bot, dp
from aiogram.types import Message
from config import my_id
from notion_scripts import change_title


async def send_to_admin(dp):
    await bot.send_message(chat_id=my_id, text="бот запущен")


@dp.message_handler()
async def echo(message: Message):
    text = message.text
    await change_title(text)
    await message.answer(text=f"я поменял название на:{text}")
