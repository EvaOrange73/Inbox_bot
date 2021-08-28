from dto.day import Day
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import DiaryColumns


def make_day(data):
    return Day(
        day_id=parse_column(data, DiaryColumns.ID),
        date=parse_column(data, DiaryColumns.DATE)
    )
