from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State

from main import dp
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_tasks import read_tasks
from utils.columns import DiaryColumns, InboxColumns
from utils.config import diary_table_id


class DayReportStates(StatesGroup):
    waiting_for_answer = State()


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

    answer += "\n\nНапиши небольшое сообщение о своей продуктивности сегодня. Почему результаты этого дня именно такие?"

    worst_context = sorted(worst_context.items(), key=lambda item: item[1], reverse=True)[0]
    answer += f"\n\nСамый непродуктивный контекст сегодня -- {worst_context[0]}"

    await message.answer(answer)
    await DayReportStates.waiting_for_answer.set()


@dp.message_handler(state=DayReportStates.waiting_for_answer)
async def process_answer(message: types.Message, state: FSMContext):
    answer = message.text

    add_page(diary_table_id, {
        DiaryColumns.NAME: "Рефлексия",
        DiaryColumns.DATE: datetime.now().date().isoformat()
    },
             children=answer
             )

    await message.answer("спасибо)")

    await state.finish()
