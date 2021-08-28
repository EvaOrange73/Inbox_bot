from dto.task import Task
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import InboxColumns


def make_task(data):

    if parse_column(data, InboxColumns.HABIT):
        task_type = "habit"
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=parse_column(data, InboxColumns.ID),
            type=task_type,
            context_id=parse_column(data, InboxColumns.CONTEXT_HABITS)
        )
    elif parse_column(data, InboxColumns.PROJECT):
        task_type = "project"
        list_of_children_id = parse_column(data, InboxColumns.CHILD)
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=parse_column(data, InboxColumns.ID),
            type=task_type,
            children=list_of_children_id
        )
    elif parse_column(data, InboxColumns.SOCIAL):
        task_type = "social_task"
        who = parse_column(data, InboxColumns.NEXT_STEP),
        description = parse_column(data, InboxColumns.DESCRIPTION)
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=parse_column(data, InboxColumns.ID),
            type=task_type
        )
    else:
        task_type = "task"
        if data.get(InboxColumns.DATE.title) is not None:
            date = parse_column(data, InboxColumns.DATE)
        else:
            date = parse_column(data, InboxColumns.SPECIAL_DATE)
        return Task(
            text=parse_column(data, InboxColumns.NAME),
            id=parse_column(data, InboxColumns.ID),
            type=task_type,
            date=date,
            context_id=parse_column(data, InboxColumns.CONTEXT_TASKS),
            parent_id=parse_column(data, InboxColumns.PARENT)
        )
