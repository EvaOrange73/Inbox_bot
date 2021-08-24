from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

from main import dp


class AllTasksState(StatesGroup):
    button = State()


@dp.message_handler(commands=['all_tasks'], state=None)
async def ask_for_note(message: types.Message):
    pass  # TODO all_tasks command
#     list_of_tasks = read_tasks().list_of_tasks
#     await message.answer(f"Актуальные задачи({len(list_of_tasks)}):")
#     await print_list_of_tasks(list_of_tasks, message)
#
#
# async def print_list_of_tasks(list_of_tasks, message: types.Message):
#     for task in list_of_tasks:
#         await message.answer(task.text, reply_markup=create_done_and_delete_keyboard(task.id))
#     await AllTasksState.button.set()
#     await message.answer("Завершить", reply_markup=end_keyboard)
#
#
# @dp.callback_query_handler(done_and_delete_buttons_callback.filter(), state=AllTasksState.button)
# async def process_delete_or_done_buttons(call: CallbackQuery, state: FSMContext, callback_data: dict):
#     await process_delete_or_done_callback(call, callback_data, state)
