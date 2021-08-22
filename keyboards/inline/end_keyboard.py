from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.common_buttons import done_and_delete_buttons_callback

end_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("конец", callback_data=done_and_delete_buttons_callback.new("end", "1"))
        ]
    ]
)
