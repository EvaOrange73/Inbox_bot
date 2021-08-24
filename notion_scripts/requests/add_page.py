from typing import Dict

import requests

from notion_scripts.form_json.form_json import form_json
from utils.columns import Column
from utils.config import headers


def add_page(table_id, data: Dict[Column, str], children=None):
    create_url = "https://api.notion.com/v1/pages"

    new_page_data = form_json(data, table_id, children=children)

    res = requests.request("POST", create_url, headers=headers, data=new_page_data)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)

    return data["id"]
