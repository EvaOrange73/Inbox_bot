from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def default_keyboard(my_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in my_list:
        keyboard.add(KeyboardButton(item))
    return keyboard
