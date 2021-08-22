from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.planning.new_tasks.categories.habit import habit
from handlers.planning.new_tasks.categories.project import project
from handlers.planning.new_tasks.categories.sotial_task import social
from handlers.planning.new_tasks.categories.task import task
from keyboards.inline.task_keyboard import task_callback, create_task_keyboard
from main import dp


async def process_single_task(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")
    list_of_tasks = data.get("list_of_tasks")
    for my_task in list_of_tasks:
        if my_task.id == task_id:
            task_text = my_task.text
            break
    else:
        task_text = ""

    await call.message.answer(task_text)
    await call.message.answer("К какой категории относится эта задача?", reply_markup=create_task_keyboard())


@dp.callback_query_handler(task_callback.filter())
async def process_yes_or_no_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    task_type = callback_data.get("type")
    await state.update_data(task_type=task_type)

    select_function = {
        "project": project,
        "habit": habit,
        "social": social,
        "task": task
    }

    await select_function[task_type](call, state)
