from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

list_callback = CallbackData("new_tasks", "item_id")


def create_list_keyboard(my_list, add_button=False):
    list_for_kb = [
        [
            InlineKeyboardButton(text=item.text, callback_data=list_callback.new(
                item_id=item.id
            ))
        ] for item in my_list
    ]
    if add_button:
        list_for_kb.append([InlineKeyboardButton(text="добавить", callback_data=list_callback.new(item_id="+"))])

    return InlineKeyboardMarkup(inline_keyboard=list_for_kb)
