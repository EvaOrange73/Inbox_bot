from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from dto.update_date import UpdateDate
from keyboards.default_keyboard import default_keyboard
from main import dp
from notion_scripts.requests.update_page import update_page
from utils.columns import InboxColumns
from utils.dates.dates import dates_for_keyboard
from utils.dates.parse_date import parse_date


class SocialTaskStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_pearson = State()
    waiting_for_time = State()


async def social(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Опиши задачу более конкретно")
    await SocialTaskStates.waiting_for_text.set()


@dp.message_handler(state=SocialTaskStates.waiting_for_text)
async def add_text_to_social_task(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Кто должен сделать следующий шаг?", reply_markup=default_keyboard(["я"]))
    await SocialTaskStates.waiting_for_pearson.set()


@dp.message_handler(state=SocialTaskStates.waiting_for_pearson)
async def add_pearson_to_social_task(message: types.Message, state: FSMContext):
    await state.update_data(next_step=message.text)
    if message.text == "я":
        await message.answer("Когда ты будешь это делать?", reply_markup=default_keyboard(dates_for_keyboard))
        await SocialTaskStates.waiting_for_time.set()
    else:
        await message.answer("задача добавлена в waiting list", reply_markup=types.ReplyKeyboardRemove())
        await end(state)
        await state.finish()


@dp.message_handler(state=SocialTaskStates.waiting_for_time)
async def add_time_to_social_task(message: Message, state: FSMContext):
    date = parse_date(message.text)
    if date is not None:
        await end(state, date)

        await message.answer(f"задача запланирована")
        await state.finish()
    else:
        await message.answer("Не получилось распознать дату, попробуй снова")


async def end(state: FSMContext, date=UpdateDate("", InboxColumns.DATE)):
    data = await state.get_data()
    task_id = data.get("task_id")
    next_step = data.get("next_step")
    description = data.get("description")
    update_page(task_id, {
        InboxColumns.SOCIAL: True,
        InboxColumns.DESCRIPTION: description,
        InboxColumns.NEXT_STEP: next_step,
        date.column: date.date,
        InboxColumns.PLANNED: True
    })
