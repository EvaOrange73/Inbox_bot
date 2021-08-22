from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

task_callback = CallbackData("task", "type")


def create_task_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="проект",
                                     callback_data=task_callback.new(type="project")),
                InlineKeyboardButton(text="привычка",
                                     callback_data=task_callback.new(type="habit"))
            ],
            [
                InlineKeyboardButton(text="требует общения",
                                     callback_data=task_callback.new(type="social")),
                InlineKeyboardButton(text="одно действие",
                                     callback_data=task_callback.new(type="task")),
            ]
        ]
    )
