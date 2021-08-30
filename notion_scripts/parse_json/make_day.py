from dto.day import Day
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import DiaryColumns


def make_day(data, arg):
    return Day(
        day_id=parse_column(data, DiaryColumns.ID),
        date=parse_column(data, DiaryColumns.DATE),
        contexts=parse_column(data, DiaryColumns.CONTEXTS),
        hangouts=parse_column(data, DiaryColumns.HANGOUTS),
        context_names=parse_column(data, DiaryColumns.CONTEXT_NAMES)
    )
