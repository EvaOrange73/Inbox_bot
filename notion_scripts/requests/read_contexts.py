import requests

from notion_scripts.parse_json.make_context import make_context
from utils.config import context_table_id, headers


def read_contexts(all_tasks, list_of_ids=False, filter_data=""):
    read_url = f"https://api.notion.com/v1/databases/{context_table_id}/query"
    res = requests.request("POST", read_url, headers=headers, data=filter_data)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
    contexts = []
    for i in range(len(data["results"])):
        if list_of_ids:
            if not (data["results"][i]["id"] in list_of_ids):
                continue
        context = make_context(data["results"][i], all_tasks)
        contexts.append(context)

    return contexts
