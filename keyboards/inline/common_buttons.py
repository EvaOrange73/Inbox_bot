from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

done_and_delete_buttons_callback = CallbackData("done_and_delete", "button_type", "task_id", "task_type")


def create_done_and_delete_keyboard(note_id, task_type):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="сделано", callback_data=done_and_delete_buttons_callback.new(
                    button_type="done",
                    task_id=note_id,
                    task_type=task_type
                )),

                InlineKeyboardButton(text="удалить", callback_data=done_and_delete_buttons_callback.new(
                    button_type="delete",
                    task_id=note_id,
                    task_type=task_type
                ))]
        ]
    )
