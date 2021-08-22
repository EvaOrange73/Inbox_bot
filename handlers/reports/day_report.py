from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State

from main import dp
from notion_scripts.requests.add_page import add_page
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.requests.read_tasks import read_tasks
from utils.columns import DiaryColumns, InboxColumns
from utils.config import diary_table_id


class DayReportStates(StatesGroup):
    waiting_for_answer = State()


@dp.message_handler(Command("day_report"))
async def day_report(message: types.Message, state: FSMContext):
    tasks = read_tasks(filter_data=equals_filter({
        InboxColumns.DELETE: False,
        InboxColumns.DONE: False,
        InboxColumns.DATE: datetime.now().date().isoformat()
    })).list_of_tasks
    if len(tasks):
        answer = "Сегодня не были сделаны следующие задачи:"
        for task in tasks:
            answer += f"\n{task.text}"
        answer += "\nНапиши пару слов о том, почему не получилось сделать запланированное"
    else:
        answer = "Сегодня были сделаны все запланированные задачи!\n" \
                 "Напиши пару слов о том, как это удалось;)"

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
