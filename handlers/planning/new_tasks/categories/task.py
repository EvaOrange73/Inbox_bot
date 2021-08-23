from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.planning.context.ask_for_context import ask_for_context
from keyboards.default_keyboard import default_keyboard
from main import dp
from notion_scripts.requests.update_page import update_page
from utils.dates.dates import get_dates_for_keyboard
from utils.dates.parse_date import parse_date


class TaskStates(StatesGroup):
    waiting_for_yes_or_no = State()
    waiting_for_date = State()
    waiting_for_when = State()
    waiting_for_context = State()


async def task(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Когда ты будешь это делать?", reply_markup=default_keyboard(get_dates_for_keyboard()))
    await TaskStates.waiting_for_date.set()


@dp.message_handler(state=TaskStates.waiting_for_date)
async def process_day(message: types.Message, state: FSMContext):
    date = parse_date(message.text)
    if date is not None:
        data = await state.get_data()
        task_id = data.get("task_id")
        update_page(task_id, {date.column: date.date})
        await ask_for_context(message, state)
    else:
        await message.answer("Не получилось распознать дату, попробуй снова")
