from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message

from dto.day_context import DayContext
from dto.item import Item
from handlers.working.get_social_tasks import get_social_tasks
from keyboards.default_keyboard import default_keyboard
from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from main import dp
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.form_json.form_day_content import form_day_content
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_contexts import read_contexts
from notion_scripts.requests.read_tasks import read_tasks
from utils.columns import DiaryColumns, InboxColumns
from utils.config import diary_table_id
from utils.properties import InboxProperties, weekday


class PlanStateOrder(StatesGroup):
    waiting_for_order = State()
    add_context = State()


def format_context(context):
    return f"{context.text}({context.get_day_quantity(datetime.now().date() + timedelta(days=1))})"


def make_list_for_keyboard(day_context):
    return [Item(id=i,
                 text=format_context(day_context.default_order[i]))
            for i in range(len(day_context.default_order))]


@dp.message_handler(Command("plan_for_tomorrow"))
async def ask_for_tomorrow_contexts(message: types.Message, state: FSMContext):
    all_tasks = read_tasks(filter_data=equals_filter({
        InboxColumns.DELETE: False,
        InboxColumns.DONE: False,
        InboxColumns.TYPE: InboxProperties.TASK.value
    }))
    await message.answer(get_social_tasks(all_tasks.list_of_social_tasks))
    await state.update_data(list_of_social_tasks=all_tasks.list_of_social_tasks)
    contexts = read_contexts(all_tasks)
    for context in contexts:
        if not context.is_planned:
            await message.answer("План на завтра не получился(( /new_context")
            await state.finish()
            break
    else:
        day_context = DayContext(contexts, datetime.now().date() + timedelta(days=1))

        await message.answer("На завтра запланированы следующие контексты. Определи их порядок",
                             reply_markup=create_list_keyboard(make_list_for_keyboard(day_context),
                                                               True))

        await state.update_data(day_context=day_context)
        await PlanStateOrder.waiting_for_order.set()


@dp.callback_query_handler(list_callback.filter(), state=PlanStateOrder.waiting_for_order)
async def process_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get("item_id")
    data = await state.get_data()
    day_context = data.get("day_context")
    if item_id == "+":
        await call.message.edit_text(call.message.text)
        list_for_kb = [context.text for context in day_context.other]
        await call.message.answer("Какой контекст ты хочешь добавить?",
                                  reply_markup=default_keyboard(list_for_kb))
        await PlanStateOrder.add_context.set()
    else:
        list_of_social_tasks = data.get("list_of_social_tasks")
        selected = day_context.default_order.pop(int(item_id))
        day_context.right_order.append(selected)
        answer = f"{call.message.text}\n{format_context(selected)}"
        await state.update_data(day_context=day_context)

        if len(day_context.default_order) > 0:
            await call.message.edit_text(answer,
                                         reply_markup=create_list_keyboard(make_list_for_keyboard(day_context), True))
        else:
            await call.message.edit_text(f"{answer}\nЗаписываю в ежедневник...")
            date = datetime.now().date() + timedelta(days=1)
            add_page(diary_table_id,
                     {
                         DiaryColumns.NAME: weekday[date.weekday()],
                         DiaryColumns.DATE: date.isoformat(),
                         DiaryColumns.CONTEXTS: [context.id for context in day_context.right_order]
                     },
                     children=form_day_content(day_context.right_order, list_of_social_tasks)
                     )

            await call.message.answer("План на завтра готов!")
            await state.finish()


@dp.message_handler(state=PlanStateOrder.add_context)
async def add_context(message: Message, state: FSMContext):
    data = await state.get_data()
    day_context = data.get("day_context")
    for context in day_context.other:
        if message.text == context.text:
            day_context.other.remove(context)
            day_context.right_order.append(context)
            await state.update_data(day_context=day_context)
            break

    answer = "На завтра запланированы следующие контексты:"
    for context in day_context.right_order:
        answer += f"\n{format_context(context)}"

    await message.answer(answer, reply_markup=create_list_keyboard(make_list_for_keyboard(day_context), True))
    await PlanStateOrder.waiting_for_order.set()
