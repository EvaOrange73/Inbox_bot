from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData("new_tasks", "answer")


def create_yes_or_no_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="да",
                                     callback_data=yes_or_no_callback.new(
                                         answer="yes"
                                     )),
                InlineKeyboardButton(text="нет",
                                     callback_data=yes_or_no_callback.new(
                                         answer="no"
                                     )),
            ]
        ]
    )
