from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from keyboards.inline.yes_or_no_keyboard import create_yes_or_no_keyboard, yes_or_no_callback
from main import dp
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.update_page import update_page
from utils.columns import DateColumns
from utils.config import date_table_id
from utils.dates.dates import get_only_special_dates_for_keyboard
from utils.dates.parse_date import parse_date


class OrderDates(StatesGroup):
    select_date = State()
    waiting_for_name = State()
    waiting_for_yes_or_no = State()
    waiting_for_date = State()


@dp.message_handler(commands=['special_dates'], state=None)
async def select_date(message: types.Message):
    await message.answer("Примерные даты",
                         reply_markup=create_list_keyboard(get_only_special_dates_for_keyboard(), add_button=True))
    await OrderDates.select_date.set()


@dp.callback_query_handler(list_callback.filter(), state=OrderDates.select_date)
async def process_date(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text(call.message.text)
    date_id = callback_data.get("item_id")
    if date_id == "+":
        await call.message.answer("Название:")
        await OrderDates.waiting_for_name.set()
    else:
        await state.update_data(date_id=date_id)
        await ask_for_date(call.message)


@dp.message_handler(state=OrderDates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await ask_for_date(message)


async def ask_for_date(message: types.Message):
    await message.answer("Дата точная?", reply_markup=create_yes_or_no_keyboard())
    await OrderDates.waiting_for_yes_or_no.set()


@dp.callback_query_handler(yes_or_no_callback.filter(), state=OrderDates.waiting_for_yes_or_no)
async def process_yes_or_no(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("answer") == "yes":
        await call.message.edit_text("Введи дату")
        await OrderDates.waiting_for_date.set()
    else:
        data = await state.get_data()
        name = data.get("name")
        if name is not None:
            add_page(date_table_id, {DateColumns.NAME: name})
            await call.message.answer("Дата добавлена")
        else:
            await call.message.answer("ну и ладно")
        await state.finish()


@dp.message_handler(state=OrderDates.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    date = parse_date(message.text)
    if date is not None:
        if name is not None:
            add_page(date_table_id, {
                DateColumns.NAME: name,
                DateColumns.IS_EXACT: True,
                DateColumns.DATE: date.date
            })
            await message.answer("Дата добавлена")
        else:
            update_page(data.get("date_id"), {
                DateColumns.IS_EXACT: True,
                DateColumns.DATE: date.date
            })
            await message.answer("Дата обновлена")
        await state.finish()
    else:
        await message.answer("Не получилось распознать дату, попробуй снова")
