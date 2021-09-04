from dto.task import Task
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import InboxColumns


def make_task(data, arg):
    if data["properties"].get(InboxColumns.DATE.title) is not None:
        date = parse_column(data, InboxColumns.DATE)
    else:
        date = parse_column(data, InboxColumns.SPECIAL_DATE)

    parent_name = parse_column(data, InboxColumns.PARENT_NAME)
    if parent_name:
        parent_name = parent_name[0]
    else:
        parent_name = ""

    return Task(
        text=parse_column(data, InboxColumns.NAME),
        task_id=parse_column(data, InboxColumns.ID),
        task_type=parse_column(data, InboxColumns.TASK_TYPE),
        children=parse_column(data, InboxColumns.CHILD),
        who=parse_column(data, InboxColumns.NEXT_STEP),
        description=parse_column(data, InboxColumns.DESCRIPTION),
        date=date,
        context_id=parse_column(data, InboxColumns.CONTEXT_TASKS),
        parent_id=parse_column(data, InboxColumns.PARENT),
        parent_name=parent_name
    )
