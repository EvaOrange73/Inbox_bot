from dto.day import Day
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import DiaryColumns


def make_day(data):
    day_id = data["id"]
    data = data["properties"]
    return Day(
        id=day_id,
        date=parse_column(data, DiaryColumns.DATE)
    )
