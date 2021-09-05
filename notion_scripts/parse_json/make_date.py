from dto.update_date import UpdateDate
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import DateColumns, InboxColumns


def make_date(data, arg):
    return UpdateDate(name=parse_column(data, DateColumns.NAME),
                      date=data["id"],
                      column=InboxColumns.SPECIAL_DATE
                      )
