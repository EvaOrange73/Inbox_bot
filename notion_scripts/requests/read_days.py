import requests

from notion_scripts.parse_json.make_day import make_day
from utils.config import diary_table_id, headers


def read_days(filter_data=""):
    read_url = f"https://api.notion.com/v1/databases/{diary_table_id}/query"
    res = requests.request("POST", read_url, headers=headers, data=filter_data)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
    days = []
    for i in range(len(data["results"])):
        day = make_day(data["results"][i]["properties"], data["results"][i]["id"])
        days.append(day)

    return days