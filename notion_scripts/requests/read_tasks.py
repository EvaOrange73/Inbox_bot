import requests

from notion_scripts.parse_json.make_task import make_task
from utils.config import inbox_table_id, headers


class Tasks:
    def __init__(self, list_of_tasks, list_of_habits, list_of_projects, list_of_social_tasks, all_tasks):
        self.all_tasks = all_tasks
        self.list_of_social_tasks = list_of_social_tasks
        self.list_of_projects = list_of_projects
        self.list_of_habits = list_of_habits
        self.list_of_tasks = list_of_tasks


def read_tasks(filter_data=""):
    read_url = f"https://api.notion.com/v1/databases/{inbox_table_id}/query"
    res = requests.request("POST", read_url, headers=headers,
                           data=filter_data)
    data = res.json()
    if data.get("status") is not None:
        print(res.text)

    all_tasks = Tasks([], [], [], [], [])
    select_list = {
        "task": all_tasks.list_of_tasks,
        "habit": all_tasks.list_of_habits,
        "project": all_tasks.list_of_projects,
        "social_task": all_tasks.list_of_social_tasks,
    }

    for i in range(len(data["results"])):
        new_task = make_task(data["results"][i])
        select_list[new_task.type].append(new_task)
        all_tasks.all_tasks.append(new_task)

    # for i in all_tasks.list_of_social_tasks:
    #     print(i.text)
    # for i in all_tasks.list_of_projects:
    #     print(i.text)
    # for i in all_tasks.list_of_habits:
    #     print(i.text)
    # for i in all_tasks.list_of_tasks:
    #     print(i.text)

    return all_tasks
