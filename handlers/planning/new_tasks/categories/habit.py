from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.planning.context.ask_for_context import ask_for_context
from keyboards.default_keyboard import default_keyboard
from main import dp
from notion_scripts.requests.update_page import update_page
from utils.columns import InboxColumns
from utils.dates.dates import dates_for_keyboard
from utils.dates.parse_date import parse_date


class HabitStates(StatesGroup):
    waiting_for_start = State()
    waiting_for_end = State()
    waiting_for_context = State()


async def habit(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Когда ты хочешь сделать это первый раз?",
                              reply_markup=default_keyboard(dates_for_keyboard))
    await HabitStates.waiting_for_start.set()


@dp.message_handler(state=HabitStates.waiting_for_start)
async def process_start(message: types.Message, state: FSMContext):
    start = parse_date(message.text)
    if start is not None:
        await state.update_data(start=start)

        await message.answer("Как ты думаешь, когда привычка перестанет быть актуальной?",
                             reply_markup=default_keyboard(dates_for_keyboard))
        await HabitStates.waiting_for_end.set()
    else:
        await message.answer("Не получилось распознать дату, попробуй снова")


@dp.message_handler(state=HabitStates.waiting_for_end)
async def process_end(message: types.Message, state: FSMContext):
    end = parse_date(message.text)
    if end is not None:
        data = await state.get_data()
        if end.column == InboxColumns.DATE:
            end_column = InboxColumns.HABIT_END
        else:
            end_column = InboxColumns.HABIT_SPECIAL_END
        start = data.get("start")
        if start.column == InboxColumns.DATE:
            start_column = InboxColumns.HABIT_START
        else:
            start_column = InboxColumns.HABIT_SPECIAL_START

        update_page(data.get("task_id"),
                    {
                        InboxColumns.HABIT: True,
                        start_column: start.date,
                        end_column: end.date,
                        InboxColumns.PLANNED: True
                    })

        await ask_for_context(message, state)
    else:
        await message.answer("Не получилось распознать дату, попробуй снова")
