from utils.properties import InboxProperties


class Tasks:
    def __init__(self, all_tasks):
        self.all_tasks = all_tasks
        list_of_social_tasks = []
        list_of_projects = []
        list_of_habits = []
        list_of_tasks = []

        select_list = {
            InboxProperties.SINGLE_TASK.value: list_of_tasks,
            InboxProperties.HABIT.value: list_of_habits,
            InboxProperties.PROJECT.value: list_of_projects,
            InboxProperties.SOCIAL_TASK.value: list_of_social_tasks,
        }

        for task in all_tasks:
            select_list[task.type].append(task)

        self.list_of_social_tasks = list_of_social_tasks
        self.list_of_projects = list_of_projects
        self.list_of_habits = list_of_habits
        self.list_of_tasks = list_of_tasks
