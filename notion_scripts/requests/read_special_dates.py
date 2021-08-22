import requests

from dto.update_date import UpdateDate
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import DateColumns, InboxColumns
from utils.config import headers, date_table_id


def read_special_dates():
    read_url = f"https://api.notion.com/v1/databases/{date_table_id}/query"
    res = requests.request("POST", read_url, headers=headers)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
    dates = {}
    for i in range(len(data["results"])):
        dates[parse_column(data["results"][i]["properties"], DateColumns.NAME)] = \
            UpdateDate(parse_column(data["results"][i]["properties"], DateColumns.DATE), InboxColumns.DATE)
    return dates
