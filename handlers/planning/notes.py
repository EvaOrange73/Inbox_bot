from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup

from keyboards.default_keyboard import default_keyboard
from keyboards.inline.task_or_info_keyboard import create_task_or_info_keyboard, task_or_info_callback
from main import dp
from notion_scripts.requests.add_page import add_page
from utils.columns import InboxColumns
from utils.config import inbox_table_id


class OrderNotes(StatesGroup):
    waiting_for_note = State()
    waiting_for_type = State()


@dp.message_handler(commands=['notes'], state=None)
async def ask_for_note(message: types.Message):
    await message.answer("заметка:", reply_markup=default_keyboard(["завершить"]))
    await OrderNotes.waiting_for_note.set()


@dp.message_handler(state=OrderNotes.waiting_for_note)
async def add_note_to_inbox(message: types.Message, state: FSMContext):
    if message.text != "завершить":
        await state.update_data(note_data={InboxColumns.NAME: message.text})
        await message.answer("Заметка добавлена. К какому типу относится эта задача?",
                             reply_markup=create_task_or_info_keyboard)
        await OrderNotes.waiting_for_type.set()
    else:
        await state.finish()


@dp.callback_query_handler(task_or_info_callback.filter(), state=OrderNotes.waiting_for_type)
async def add_note_type(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    note_type = callback_data.get("type")
    data = await state.get_data()
    note_data = data.get("note_data")
    note_data[InboxColumns.TYPE] = callback_data.get("type")
    add_page(inbox_table_id, note_data)
    await call.message.edit_text(f" это {note_type}", reply_markup=InlineKeyboardMarkup())
    await call.message.answer("следующая заметка:")
    await OrderNotes.waiting_for_note.set()
