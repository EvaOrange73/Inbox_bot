from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from dto.context import Context
from handlers.planning.context.new_context import ContextStates
from keyboards.default_keyboard import default_keyboard
from keyboards.inline.yes_or_no_keyboard import create_yes_or_no_keyboard
from main import dp
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_table import read_table
from notion_scripts.requests.update_page import update_page
from utils.columns import InboxColumns, ContextColumns
from utils.config import context_table_id


async def ask_for_context(message: types.Message, state: FSMContext):
    list_of_contexts = read_table(context_table_id)

    await state.update_data(list_of_contexts=list_of_contexts)
    await message.answer("Каким должен быть контекст?", reply_markup=default_keyboard(
        [context.text for context in list_of_contexts]
    ))
    await ContextStates.waiting_for_chose_context.set()


@dp.message_handler(state=ContextStates.waiting_for_chose_context)
async def process_context(message: types.Message, state: FSMContext):
    data = await state.get_data()
    list_of_contexts = data.get("list_of_contexts")

    for context_item in list_of_contexts:
        if context_item.text == message.text:
            context = context_item
            break
    else:
        new_context_id = add_page(context_table_id, {ContextColumns.NAME: message.text})
        context = Context(message.text, new_context_id, False)

    data = await state.get_data()
    task_id = data.get("task_id")
    task_type = data.get("task_type")

    select_column = {
        "project": InboxColumns.CONTEXT_PROJECTS,
        "habit": InboxColumns.CONTEXT_HABITS,
        "social": InboxColumns.CONTEXT_SOCIALS,
        "task": InboxColumns.CONTEXT_TASKS
    }

    update_page(task_id, {
        select_column[task_type]: context.id,
        InboxColumns.PLANNED: True
    })

    if task_type == "project":
        data = await state.get_data()
        list_of_tasks = data.get("list_of_tasks")

        project_id = data.get("task_id")
        update_page(project_id, {InboxColumns.CONTEXT_PROJECTS: context.id})
        for task in list_of_tasks:
            update_page(task.id, {InboxColumns.CONTEXT_TASKS: context.id})  # TODO миллион лишних запросов

        await end(message, state)

    else:
        await message.answer("Задача запланирована", reply_markup=types.ReplyKeyboardRemove())

    await state.finish()

    if not context.is_planned:
        await state.update_data(context_id=context.id)
        await message.answer("Это новый контекст, хочешь подумать о нём сейчас?",
                             reply_markup=create_yes_or_no_keyboard())
        await ContextStates.waiting_for_yes_or_no.set()


async def end(message: Message, state: FSMContext):
    data = await state.get_data()
    list_of_tasks = data.get("list_of_tasks")
    date = data.get("date")
    context = data.get("context")
    project_id = data.get("task_id")
    update_page(project_id, {InboxColumns.PLANNED: True})
    if date:
        if context:
            await message.answer("Проект и подзадачи запланированы")
            for task in list_of_tasks:
                update_page(task.id, {InboxColumns.PLANNED: True})
        else:
            await message.answer(
                "Проект запланирован. Индивидуальные контексты подзадачам можно добавить через /new_tasks")
    else:
        await message.answer("Проект запланирован. Запланировать выполнение подзадач можно через /new_tasks")
