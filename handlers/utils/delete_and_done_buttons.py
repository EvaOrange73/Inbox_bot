from aiogram import types
from aiogram.dispatcher import FSMContext

from notion_scripts.requests.update_page import update_page
from utils.columns import InboxColumns
from utils.properties import InboxProperties


async def process_delete_or_done_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("type") == "done":
        update_page(callback_data.get("note_id"), {
            InboxColumns.TYPE: InboxProperties.TASK.value,
            InboxColumns.DONE: True
        })
        await call.message.edit_text(f"задача \"{call.message.text}\" сделана")
    elif callback_data.get("type") == "delete":
        update_page(callback_data.get("note_id"), {
            InboxColumns.DELETE: True
        })
        await call.message.edit_text(f"заметка \"{call.message.text}\" удалена")
    elif callback_data.get("type") == "end":
        await state.finish()
        await call.message.edit_text("завершено")
