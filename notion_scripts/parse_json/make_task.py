from dto.task import Task
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import InboxColumns


def make_task(data):
    task_id = data["id"]
    data = data["properties"]

    if parse_column(data, InboxColumns.HABIT):
        task_type = "habit"
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=task_id,
            type=task_type
        )
    elif parse_column(data, InboxColumns.PROJECT):
        task_type = "project"
        list_of_children_id = parse_column(data, InboxColumns.CHILD)
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=task_id,
            type=task_type
        )
    elif parse_column(data, InboxColumns.SOCIAL):
        task_type = "social_task"
        who = parse_column(data, InboxColumns.NEXT_STEP),
        description = parse_column(data, InboxColumns.DESCRIPTION)
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=task_id,
            type=task_type
        )
    else:
        task_type = "task"
        print(data)
        if data.get(InboxColumns.DATE.title) is not None:
            date = parse_column(data, InboxColumns.DATE)
        else:
            date = parse_column(data, InboxColumns.WHEN)
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=task_id,
            type=task_type,
            date=date
        )
