import requests

from notion_scripts.parse_json.make_reflection import make_reflection
from utils.config import reflection_table_id, headers


def read_reflections(filter_data=""):
    read_url = f"https://api.notion.com/v1/databases/{reflection_table_id}/query"
    res = requests.request("POST", read_url, headers=headers, data=filter_data)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
    reflections = []
    for i in range(len(data["results"])):
        reflection = make_reflection(data["results"][i]["properties"], data["results"][i]["id"])
        reflections.append(reflection)

    return reflections
