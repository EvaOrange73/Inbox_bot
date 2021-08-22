from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from dto.task import Task
from handlers.planning.context.ask_for_context import ask_for_context, end
from keyboards.default_keyboard import default_keyboard
from keyboards.inline.yes_or_no_keyboard import create_yes_or_no_keyboard, yes_or_no_callback
from main import dp
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.update_page import update_page
from utils.columns import InboxColumns
from utils.config import inbox_table_id
from utils.dates.dates import dates_for_keyboard
from utils.dates.parse_date import parse_date
from utils.properties import InboxProperties


class ProjectStates(StatesGroup):
    waiting_for_tasks = State()
    waiting_for_same_date = State()
    waiting_for_date = State()
    waiting_for_same_context = State()
    waiting_for_context = State()


async def project(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")
    update_page(task_id, {
        InboxColumns.PROJECT: True
    })

    await call.message.answer("Добавь подзадачу")
    await state.update_data(list_of_tasks=[])
    await ProjectStates.waiting_for_tasks.set()


@dp.message_handler(state=ProjectStates.waiting_for_tasks)
async def process_task(message: Message, state: FSMContext):
    if message.text != "завершить":
        task_text = message.text
        data = await state.get_data()
        project_id = data.get("task_id")

        task_id = add_page(inbox_table_id, {
            InboxColumns.NAME: message.text,
            InboxColumns.TYPE: InboxProperties.TASK.value,
            InboxColumns.PARENT: project_id
        })

        new_task = Task(task_text, task_id, True)
        data = await state.get_data()
        list_of_tasks = data.get("list_of_tasks")
        list_of_tasks.append(new_task)
        await state.update_data(list_of_tasks=list_of_tasks)

        await message.answer("Подзадача добавлена. Го следующую", reply_markup=default_keyboard(["завершить"]))
    else:
        await message.answer("Все эти задачи относятся к одной дате?", reply_markup=create_yes_or_no_keyboard())
        await ProjectStates.waiting_for_same_date.set()


@dp.callback_query_handler(yes_or_no_callback.filter(), state=ProjectStates.waiting_for_same_date)
async def process_same_date(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("answer") == "yes":
        await state.update_data(date=1)
        await call.message.answer("Когда ты выполнишь проект?", reply_markup=default_keyboard(dates_for_keyboard))
        await ProjectStates.waiting_for_date.set()
    else:
        await state.update_data(date=0)
        await ask_about_same_context(call.message)


@dp.message_handler(state=ProjectStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
    date = parse_date(message.text)

    data = await state.get_data()
    list_of_tasks = data.get("list_of_tasks")
    project_id = data.get("task_id")

    update_page(project_id, {date.column: date.date})
    for task in list_of_tasks:
        update_page(task.id, {date.column: date.date})  # TODO миллион лишних запросов
    await ask_about_same_context(message)


async def ask_about_same_context(message: Message):
    await message.answer("Все подзадачи относятся к тому же контексту, что и проект?",
                         reply_markup=create_yes_or_no_keyboard())
    await ProjectStates.waiting_for_same_context.set()


@dp.callback_query_handler(yes_or_no_callback.filter(), state=ProjectStates.waiting_for_same_context)
async def process_same_date(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("answer") == "yes":
        await state.update_data(context=1)
        await ask_for_context(call.message, state)
    else:
        await state.update_data(context=0)
        await end(call.message, state)
