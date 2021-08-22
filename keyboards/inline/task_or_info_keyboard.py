from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

task_or_info_callback = CallbackData("task_or_info", "type")
there_are_all_tasks_callback = CallbackData("there_are_all_tasks", "name")

create_task_or_info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="задача", callback_data=task_or_info_callback.new(
                type="задача"
            )),
            InlineKeyboardButton(text="инфа", callback_data=task_or_info_callback.new(
                type="инфа"
            ))
        ],
    ]
)

there_are_all_tasks_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="да", callback_data=there_are_all_tasks_callback.new(
                name="task_or_info"
            )),

        ]
    ]
)
