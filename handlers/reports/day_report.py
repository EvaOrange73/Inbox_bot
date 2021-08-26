from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.default_keyboard import default_keyboard
from main import dp
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_tasks import read_tasks
from utils.columns import ReflectionColumns, InboxColumns
from utils.config import reflection_table_id
from utils.properties import ReflectionProperties, weekday


class DayReportStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_productivity = State()


@dp.message_handler(Command("day_report"))
async def day_report(message: types.Message, state: FSMContext):
    all_tasks = read_tasks(filter_data=equals_filter({
        InboxColumns.DELETE: False,
        InboxColumns.DONE: False,
        InboxColumns.DATE: datetime.now().date().isoformat()
    }))
    worst_context = {}
    tasks = all_tasks.list_of_tasks
    if len(tasks):
        answer = "Сегодня не были сделаны задачи:"
        for task in tasks:
            answer += f"\n{task.text}({task.context_name})"
            context = worst_context.get(task.context_name)
            if context is None:
                context = 0
            worst_context[task.context_name] = context + 1
    else:
        answer = "Сегодня были сделаны все запланированные задачи!"

    habits = all_tasks.list_of_habits
    if len(habits):
        answer += "\n\nНе были выполнены привычки:"
        for habit in habits:
            answer += f"\n{habit.text}({habit.context_name})"
            context = worst_context.get(habit.context_name)
            if context is None:
                context = 0
            worst_context[habit.context_name] = context + 1
    else:
        answer += "\n\nБыли выполнены все привычки!"

    projects = all_tasks.list_of_projects
    if len(projects):
        answer += "\n\nСейчас в процессе находятся проекты:"
        for project in projects:
            answer += f"\n{project.text}(осталось задач: {len(project.children)})"
    else:
        answer += "\n\nНет актуальных проектов"

    socials = all_tasks.list_of_social_tasks
    if len(socials):
        answer += "\n\nВ процессе находятся следующие взаимодействия:"
        for social in socials:
            answer += f"{social.text}"
    else:
        answer += "\n\nНет текущих социальных взаимодействий"

    answer += "\n\nДай название сегодняшнему дню!"

    if worst_context:
        worst_context = sorted(worst_context.items(), key=lambda item: item[1], reverse=True)[0]
        await state.update_data(worst_context=worst_context[0])
        answer += f"\n\nСамый непродуктивный контекст сегодня -- {worst_context[0]}"

    await message.answer(answer, reply_markup=default_keyboard([weekday[datetime.now().weekday()]]))
    await DayReportStates.waiting_for_name.set()


@dp.message_handler(state=DayReportStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    answer = "Напиши небольшое сообщение о своей продуктивности сегодня"

    data = await state.get_data()
    worst_context = data.get("worst_context")
    if worst_context is not None:
        answer += f"\nСамый непродуктивный контекст -- {worst_context}"
    answer += "\n\nПочему результаты этого дня именно такие?"

    await message.answer(answer)
    await DayReportStates.waiting_for_productivity.set()


@dp.message_handler(state=DayReportStates.waiting_for_productivity)
async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()

    add_page(reflection_table_id, {
        ReflectionColumns.NAME: data.get("name"),
        ReflectionColumns.TYPE: ReflectionProperties.DAY.value,
        ReflectionColumns.DATE: datetime.now().date().isoformat(),
        ReflectionColumns.PRODUCTIVITY: message.text
    })

    await message.answer("спасибо)")
    await state.finish()
