from typing import Dict, Union, Any

import requests

from notion_scripts.form_json.form_json import form_json
from utils.columns import InboxColumns, ContextColumns, Column
from utils.config import headers


def update_page(line_id, data: Dict[Column, Any], children=None):
    update_url = f"https://api.notion.com/v1/pages/{line_id}"

    update_data = form_json(data, children=children)

    res = requests.request("PATCH", update_url, headers=headers, data=update_data)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
