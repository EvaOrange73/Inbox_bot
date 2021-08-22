from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

done_and_delete_buttons_callback = CallbackData("done_and_delete", "type", "note_id")


def add_done_and_delete_buttons(note_id):
    return [
        InlineKeyboardButton(text="сделано", callback_data=done_and_delete_buttons_callback.new(
            type="done",
            note_id=note_id
        )),

        InlineKeyboardButton(text="удалить", callback_data=done_and_delete_buttons_callback.new(
            type="delete",
            note_id=note_id
        ))]


def create_done_and_delete_keyboard(note_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            add_done_and_delete_buttons(note_id)
        ]
    )


def undo_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="назад ↩", callback_data="undo")
            ]
        ]
    )
