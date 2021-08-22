from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from dto.item import Item
from handlers.planning.context.context_states import ContextStates
from keyboards.inline.list_keyboard import create_list_keyboard, list_callback
from keyboards.inline.time_keyboard import time_keyboard, time_callback
from keyboards.inline.yes_or_no_keyboard import yes_or_no_callback
from main import dp
from notion_scripts.requests.update_page import update_page
from notion_scripts.form_json.ecuals_filter import equals_filter
from notion_scripts.requests.read_contexts import read_contexts
from utils.columns import ContextColumns


@dp.callback_query_handler(yes_or_no_callback.filter(), state=ContextStates.waiting_for_yes_or_no)
async def process_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("answer") == "yes":
        await ask_for_time(call)
    else:
        await call.message.edit_text("Это новый контекст. Я спрошу о нём позже.")
        await state.finish()


@dp.message_handler(Command("new_context"))
async def select_context(message: types.Message, state: FSMContext):
    list_of_contexts = read_contexts([], filter_data=equals_filter(
        {
            ContextColumns.DELETE: False,
            ContextColumns.DESCRIPTION: False
        }
    ))
    await state.update_data(list_of_contexts=list_of_contexts)
    list_for_kb = [Item(context.text, context.id) for context in list_of_contexts]
    if len(list_of_contexts) > 0:
        await message.answer("Какой контекст ты хочешь описать?", reply_markup=create_list_keyboard(list_for_kb))
        await ContextStates.waiting_for_chose_context.set()
    else:
        await message.answer("Нет новых контекстов")  # TODO тут должна быть возможность добавить новый контекст


@dp.callback_query_handler(list_callback.filter(), state=ContextStates.waiting_for_chose_context)
async def process_select_context(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    context_id = callback_data.get("item_id")
    data = await state.get_data()
    list_of_contexts = data.get("list_of_contexts")
    context_text = ""
    for context in list_of_contexts:
        if context.id == context_id:
            context_text = context.text
    await state.update_data(context_id=context_id)
    await call.message.edit_text(context_text)
    await ask_for_time(call)


async def ask_for_time(call: types.CallbackQuery):
    await call.message.answer("К какому времени суток относится этот контекст?", reply_markup=time_keyboard)
    await ContextStates.waiting_for_time.set()


@dp.callback_query_handler(time_callback.filter(), state=ContextStates.waiting_for_time)
async def process_time(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(time=callback_data.get("time"))
    await call.message.answer(
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
    context_id = data.get("context_id")
    conditions = data.get("conditions")
    time = data.get("time")
    update_page(context_id, {
        ContextColumns.RESULT: message.text,
        ContextColumns.CONDITIONS: conditions,
        ContextColumns.DESCRIPTION: True,
        ContextColumns.TIME: time
    })
    await message.answer("Описание контекста добавлено")
    await state.finish()
