import requests

from utils.config import headers


def read_page_content(page_id):
    read_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    res = requests.request("GET", read_url, headers=headers)
    data = res.json()
    if data.get("status") == 400:
        print(res.text)
    return res.text
