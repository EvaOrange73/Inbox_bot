import requests

from utils.config import headers


def read_line(page_id):
    read_url = f"https://api.notion.com/v1/pages/{page_id}"
    res = requests.request("GET", read_url, headers=headers)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
    return data["properties"]["Name"]["title"][0]['plain_text']


class Task:
    def __init__(self, text, task_id, task_type, who="", description="", date="", parent_id="", parent_name="", context_id="",
                 children=""):
        self.description = description
        self.who = who
        self.type = task_type
        self.text = text
        self.id = task_id
        self.date = date
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.context_id = context_id
        if context_id:
            self.context_name = read_line(context_id[0])  # TODO лишний запрос
        else:
            self.context_name = ""
        self.children = children
