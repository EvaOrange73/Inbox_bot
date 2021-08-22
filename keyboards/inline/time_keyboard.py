from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

time_callback = CallbackData("new_tasks", "time")

time_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="утро",
                                 callback_data=time_callback.new(
                                     time="утро"
                                 )),
            InlineKeyboardButton(text="день",
                                 callback_data=time_callback.new(
                                     time="день"
                                 )),
            InlineKeyboardButton(text="вечер",
                                 callback_data=time_callback.new(
                                     time="вечер"
                                 ))
        ], [
            InlineKeyboardButton(text="-",
                                 callback_data=time_callback.new(
                                     time="-"
                                 ))
        ]
    ]
)
