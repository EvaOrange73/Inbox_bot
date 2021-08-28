import requests

from notion_scripts.parse_json.make_context import make_context
from notion_scripts.parse_json.make_day import make_day
from notion_scripts.parse_json.make_reflection import make_reflection
from notion_scripts.parse_json.make_task import make_task
from utils.config import headers, context_table_id, inbox_table_id, reflection_table_id, diary_table_id


def read_table(table_id, filter_data="", all_tasks=None, list_of_ids=False):
    read_url = f"https://api.notion.com/v1/databases/{table_id}/query"
    res = requests.request("POST", read_url, headers=headers, data=filter_data)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)

    select_function = {
        context_table_id: make_context,
        inbox_table_id: make_task,
        reflection_table_id: make_reflection,
        diary_table_id: make_day

    }

    lines = []
    for i in range(len(data["results"])):
        if list_of_ids:
            if not (data["results"][i]["id"] in list_of_ids):
                continue
        line = select_function[table_id](data["results"][i], all_tasks)
        lines.append(line)

    return lines
