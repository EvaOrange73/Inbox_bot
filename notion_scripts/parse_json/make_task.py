from dto.task import Task
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import InboxColumns


def make_task(data, arg):
    if parse_column(data, InboxColumns.HABIT):
        task_type = "habit"
    elif parse_column(data, InboxColumns.PROJECT):
        task_type = "project"
    elif parse_column(data, InboxColumns.SOCIAL):
        task_type = "social_task"
    else:
        task_type = "task"

    if data["properties"].get(InboxColumns.DATE.title) is not None:
        date = parse_column(data, InboxColumns.DATE)
    else:
        date = parse_column(data, InboxColumns.SPECIAL_DATE)

    return Task(
        text=parse_column(data, InboxColumns.NAME),
        task_id=parse_column(data, InboxColumns.ID),
        task_type=task_type,
        children=parse_column(data, InboxColumns.CHILD),
        who=parse_column(data, InboxColumns.NEXT_STEP),
        description=parse_column(data, InboxColumns.DESCRIPTION),
        date=date,
        context_id=parse_column(data, InboxColumns.CONTEXT_TASKS),
        parent_id=parse_column(data, InboxColumns.PARENT)
    )
