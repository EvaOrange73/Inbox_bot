from aiogram.dispatcher.filters.state import StatesGroup, State


class ContextStates(StatesGroup):
    waiting_for_new_context = State()
    waiting_for_context = State()
    waiting_for_yes_or_no = State()
    waiting_for_chose_context = State()
    waiting_for_conditions = State()
    waiting_for_result = State()
