from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from main import dp
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.update_page import update_page
from utils.columns import ReflectionColumns
from utils.config import reflection_table_id
from utils.properties import ReflectionProperties


class SmallPeriodReflectionStates(StatesGroup):
    waiting_for_productivity = State()


async def small_period_reflection(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_reflections = data.get("new_reflections")
    await state.update_data(period=f"{new_reflections[0].date} -- {new_reflections[-1].date}")
    answer = "Ты делала такие заметки о продуктивности:"
    for reflection in new_reflections:
        answer += f"\n\n{reflection.name}: {reflection.productivity}"
    answer += "\n\nПопробуй обобщить эти заметки"
    await message.answer(answer)
    await SmallPeriodReflectionStates.waiting_for_productivity.set()


@dp.message_handler(state=SmallPeriodReflectionStates.waiting_for_productivity)
async def process_productivity(message: types.Message, state: FSMContext):
    data = await state.get_data()
    period = data.get("period")
    new_reflections = data.get("new_reflections")
    add_page(reflection_table_id, {
        ReflectionColumns.NAME: period,
        ReflectionColumns.TYPE: ReflectionProperties.SMALL_PERIOD.value,
        ReflectionColumns.PRODUCTIVITY: message.text,
        ReflectionColumns.CHILD: [reflection.id for reflection in new_reflections]
    })
    for reflection in new_reflections:
        update_page(reflection.id, {
            ReflectionColumns.IS_PROCESSED: True
        })

    await message.answer("Спасибо! Ответ записан")
    await state.finish()
