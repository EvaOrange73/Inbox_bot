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
    def __init__(self, text, id, type, date="", parent_id="", ):
        self.type = type
        self.text = text
        self.id = id
        self.date = date
        self.parent_id = parent_id
        if parent_id:
            self.parent_name = read_line(parent_id)  # TODO лишний запрос
        else:
            self.parent_name = ""
