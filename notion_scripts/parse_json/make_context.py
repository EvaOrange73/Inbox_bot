from dto.context import Context
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import ContextColumns


def make_context(data, all_tasks):
    context_id = data["id"]
    data = data["properties"]
    is_planned = parse_column(data, ContextColumns.DESCRIPTION)

    if is_planned:
        tasks = []
        habits = []
        ids = parse_column(data, ContextColumns.TASKS)

        if all_tasks:
            for task in all_tasks.list_of_tasks:
                if task.id in ids:
                    tasks.append(task)
            for habit in all_tasks.list_of_habits:
                if habit.id in ids:
                    habits.append(habit)

        return Context(
            text=parse_column(data, ContextColumns.NAME),
            id=context_id,
            time=parse_column(data, ContextColumns.TIME),
            start=parse_column(data, ContextColumns.CONDITIONS),
            end=parse_column(data, ContextColumns.RESULT),
            all_tasks=tasks,
            habits=habits,
            is_planned=True
        )
    else:
        return Context(
            text=parse_column(data, ContextColumns.NAME),
            id=context_id,
            is_planned=False
        )
