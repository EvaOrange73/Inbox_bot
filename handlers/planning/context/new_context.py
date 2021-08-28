from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from dto.item import Item
from handlers.planning.context.context_states import ContextStates
from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from keyboards.inline.yes_or_no_keyboard import yes_or_no_callback
from main import dp
from notion_scripts.form_json.equals_filter import equals_filter
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_table import read_table
from notion_scripts.requests.update_page import update_page
from utils.columns import ContextColumns
from utils.config import context_table_id


@dp.callback_query_handler(yes_or_no_callback.filter(), state=ContextStates.waiting_for_yes_or_no)
async def process_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("answer") == "yes":
        await ask_for_conditions(call.message)
    else:
        await call.message.edit_text("Это новый контекст. Я спрошу о нём позже.")
        await state.finish()


@dp.message_handler(Command("new_context"))
async def select_context(message: types.Message, state: FSMContext):
    list_of_contexts = read_table(context_table_id, filter_data=equals_filter({
        ContextColumns.DELETE: False,
        ContextColumns.DESCRIPTION: False
    }))
    await state.update_data(list_of_contexts=list_of_contexts)
    list_for_kb = [Item(context.text, context.id) for context in list_of_contexts]
    list_for_kb.append(Item("добавить", "add"))
    list_for_kb.append(Item("завершить", "end"))
    if len(list_of_contexts) > 0:
        await message.answer("Какой контекст ты хочешь описать?", reply_markup=create_list_keyboard(list_for_kb))
    else:
        await message.answer("Нет новых контекстов",
                             reply_markup=create_list_keyboard([Item("добавить", "add"), Item("завершить", "end")]))
    await ContextStates.waiting_for_chose_context.set()


@dp.callback_query_handler(list_callback.filter(), state=ContextStates.waiting_for_chose_context)
async def process_select_context(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    context_id = callback_data.get("item_id")
    await call.message.edit_text(call.message.text)
    if context_id == "end":
        await state.finish()
    elif context_id == "add":
        await ask_for_new_context(call.message)
    else:
        data = await state.get_data()
        list_of_contexts = data.get("list_of_contexts")
        context_text = ""
        for context in list_of_contexts:
            if context.id == context_id:
                context_text = context.text
        await state.update_data(context_id=context_id)
        await call.message.edit_text(context_text)
        await ask_for_conditions(call.message)


async def ask_for_new_context(message: Message):
    await message.answer("Новый контекст:")
    await ContextStates.waiting_for_new_context.set()


@dp.message_handler(state=ContextStates.waiting_for_new_context)
async def process_new_context(message: Message, state: FSMContext):
    await state.update_data(new_context=message.text)
    await ask_for_conditions(message)


async def ask_for_conditions(message: Message):
    await message.answer(
        "Опиши внешние условия и внутренние состояния, которые нужны для вхождения в этот контекст",
    )
    await ContextStates.waiting_for_conditions.set()


@dp.message_handler(state=ContextStates.waiting_for_conditions)
async def process_conditions(message: types.Message, state: FSMContext):
    await state.update_data(conditions=message.text)
    await message.answer("А теперь опиши результат, к которому ты придёшь на выходе из контекста")
    await ContextStates.waiting_for_result.set()


@dp.message_handler(state=ContextStates.waiting_for_result)
async def process_result(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_context = data.get("new_context")
    conditions = data.get("conditions")
    if new_context is not None:
        add_page(context_table_id, {
            ContextColumns.NAME: new_context,
            ContextColumns.RESULT: message.text,
            ContextColumns.CONDITIONS: conditions,
            ContextColumns.DESCRIPTION: True,
        })
    else:
        context_id = data.get("context_id")
        update_page(context_id, {
            ContextColumns.RESULT: message.text,
            ContextColumns.CONDITIONS: conditions,
            ContextColumns.DESCRIPTION: True,
        })
    await message.answer("Описание контекста добавлено")
    await state.finish()
