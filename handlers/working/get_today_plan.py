from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State

from dto.item import Item
from handlers.utils.delete_and_done_buttons import process_delete_or_done_callback
from handlers.working.get_social_tasks import get_social_tasks
from keyboards.inline.common_buttons import create_done_and_delete_keyboard, done_and_delete_buttons_callback
from keyboards.inline.end_keyboard import end_keyboard
from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from main import dp
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.requests.read_contexts import read_contexts
from notion_scripts.requests.read_tasks import read_tasks
from utils.columns import InboxColumns
from utils.group_by_projects import group_by_projects
from utils.properties import InboxProperties


class TodayStates(StatesGroup):
    waiting_for_context = State()
    delete_and_done = State()


def format_context(context):
    return f"{context.text}({context.get_day_quantity(datetime.now().date())})"


def make_list_for_keyboard(day_context):
    return [Item(id=i,
                 text=format_context(day_context[i]))
            for i in range(len(day_context))]


@dp.message_handler(Command("get_today_plan"))
async def ask_for_tomorrow_contexts(message: types.Message, state: FSMContext):
    all_tasks = read_tasks(filter_data=equals_filter({
        InboxColumns.DELETE: False,
        InboxColumns.DONE: False,
        InboxColumns.TYPE: InboxProperties.TASK.value,
        InboxColumns.DATE: datetime.now().date().isoformat()  # TODO подумоть.... тут тогда привычки не вернутся
    }))

    await message.answer(get_social_tasks(all_tasks.list_of_social_tasks))
    contexts = read_contexts(all_tasks)
    if contexts is None:
        await message.answer("план на сегодня не получился, так как не все контексты запланированы /new_context")
        await state.finish()
    else:
        list_for_kb = make_list_for_keyboard(contexts)
        await message.answer("На сегодня запланированы следующие контексты:",
                             reply_markup=create_list_keyboard(list_for_kb))

        await TodayStates.waiting_for_context.set()
        await state.update_data(contexts=contexts)


@dp.callback_query_handler(list_callback.filter(), state=TodayStates.waiting_for_context)
async def process_context(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    contexts = data.get("contexts")
    context_id = int(callback_data.get("item_id"))
    context = contexts[context_id]
    await call.message.answer(context.text + ":")
    await call.message.answer("Привычки:")
    for habit in context.habits:
        await call.message.answer(habit.text, reply_markup=create_done_and_delete_keyboard(habit.id))
    await call.message.answer("Задачи:")
    for project in group_by_projects(context.all_tasks):
        if project.name != "":
            await call.message.answer(project.name)
        for task in project.list_of_tasks:
            await call.message.answer(task.text, reply_markup=create_done_and_delete_keyboard(task.id))

    await TodayStates.delete_and_done.set()

    await call.message.answer(f"работа над задачами началась в {datetime.now().hour}:{datetime.now().minute}",
                              reply_markup=end_keyboard)


@dp.callback_query_handler(done_and_delete_buttons_callback.filter(), state=TodayStates.delete_and_done)
async def process_buttons(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("type") == "end":
        await call.message.edit_text(
            f"{call.message.text}\nи закончилась в {datetime.now().hour}:{datetime.now().minute}")
        await state.finish()
    else:
        await process_delete_or_done_callback(call, callback_data, state)
