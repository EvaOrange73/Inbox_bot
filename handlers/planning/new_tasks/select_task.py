from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.planning.new_tasks.select_category import process_single_task
from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from main import dp
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.requests.read_tasks import read_tasks
from utils.columns import InboxColumns


class NewTaskStates(StatesGroup):
    waiting_for_task = State()


@dp.message_handler(Command("new_tasks"), state="*")
async def new_tasks_handler(message: types.Message, state: FSMContext):
    list_of_tasks = read_tasks(filter_data=equals_filter({
        InboxColumns.DONE: False,
        InboxColumns.DELETE: False,
        InboxColumns.PLANNED: False
    })).all_tasks
    await state.update_data(list_of_tasks=list_of_tasks)
    if len(list_of_tasks) > 0:
        await message.answer("новые задачи:", reply_markup=create_list_keyboard(list_of_tasks))
        await NewTaskStates.waiting_for_task.set()
    else:
        await message.answer("новых задач нет")


@dp.callback_query_handler(list_callback.filter(), state=NewTaskStates.waiting_for_task)
async def process_new_tasks_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    list_of_tasks = data.get("list_of_tasks")
    await state.finish()
    await state.update_data(list_of_tasks=list_of_tasks)
    task_id = callback_data.get("item_id")
    await state.update_data(task_id=task_id)
    await process_single_task(call, state)
