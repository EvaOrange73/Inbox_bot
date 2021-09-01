from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State

from dto.item import Item
from handlers.reflection.small_period_reflection import small_period_reflection
from keyboards.default_keyboard import default_keyboard
from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from main import dp
from notion_scripts.form_json.equals_filter import equals_filter
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_table import read_table
from utils.columns import ReflectionColumns, InboxColumns, DiaryColumns
from utils.config import reflection_table_id, diary_table_id, inbox_table_id
from utils.properties import ReflectionProperties, weekday
from utils.tasks import Tasks


class DayReportStates(StatesGroup):
    waiting_for_handouts_description = State()
    waiting_for_name = State()
    waiting_for_productivity = State()
    if_small_reflection = State()


@dp.message_handler(Command("day_reflection"))
async def day_report(message: types.Message, state: FSMContext):
    day = read_table(diary_table_id, equals_filter({DiaryColumns.DATE: datetime.now().date().isoformat()}))[0]
    await state.update_data(day=day)
    if day.hangout_names:
        answer = "Сегодня были тусовки!"
        for hangout in day.hangout_names:
            answer += f"\n{hangout}"
        answer += "\nНапиши о том, как всё прошло!"
        await message.answer(answer)
        await DayReportStates.waiting_for_handouts_description.set()
    else:
        await print_tasks(state, message)


@dp.message_handler(state=DayReportStates.waiting_for_handouts_description)
async def process_hangouts_description(message: types.Message, state: FSMContext):
    hangouts_description = message.text
    await state.update_data(hangouts_description=hangouts_description)
    await print_tasks(state, message)


async def print_tasks(state: FSMContext, message: types.Message):
    all_tasks = Tasks(read_table(inbox_table_id, filter_data=equals_filter({
        InboxColumns.DELETE: False,
        InboxColumns.DONE: False,
        InboxColumns.DATE: datetime.now().date().isoformat()
    })))
    worst_context = {}
    tasks = all_tasks.list_of_tasks
    if tasks:
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
    if habits:
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
    if projects:
        answer += "\n\nСейчас в процессе находятся проекты:"
        for project in projects:
            answer += f"\n{project.text}(осталось задач: {len(project.children)})"
    else:
        answer += "\n\nНет актуальных проектов"

    socials = all_tasks.list_of_social_tasks
    if socials:
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

    day_id = data.get("day").id
    hangouts = data.get("hangouts_description")

    add_page(reflection_table_id, {
        ReflectionColumns.NAME: data.get("name"),
        ReflectionColumns.TYPE: ReflectionProperties.DAY.value,
        ReflectionColumns.DATE: datetime.now().date().isoformat(),
        ReflectionColumns.PRODUCTIVITY: message.text,
        ReflectionColumns.DAY_TASKS: day_id,
        ReflectionColumns.HANGOUTS: hangouts
    })

    new_reflections = read_table(reflection_table_id, filter_data=equals_filter({
        ReflectionColumns.IS_PROCESSED: False,
        ReflectionColumns.TYPE: ReflectionProperties.DAY.value
    }))
    if len(new_reflections) > 4:
        await state.update_data(new_reflections=new_reflections)
        await message.answer(f"Есть ли у тебя настроение более глубоко погрузиться в рефлексию?\n"
                             f"Не обработано {len(new_reflections)} дней",
                             reply_markup=create_list_keyboard([Item("да", "yes"), Item("нет", "no")]))
        await DayReportStates.if_small_reflection.set()
    else:
        await message.answer("спасибо за мысли об этом дне!")
        await state.finish()


@dp.callback_query_handler(list_callback.filter(), state=DayReportStates.if_small_reflection)
async def process_if_small_reflection(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text("спасибо за мысли об этом дне!")
    if callback_data.get("item_id") == "no":
        await state.finish()
    else:
        await small_period_reflection(call.message, state)
