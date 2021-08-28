from dto.Day import Day
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import DiaryColumns


def make_day(data, id):
    return Day(
        id=id,
        date=parse_column(data, DiaryColumns.DATE)
    )
