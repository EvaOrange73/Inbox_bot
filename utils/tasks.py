class Tasks:
    def __init__(self, all_tasks):
        self.all_tasks = all_tasks
        list_of_social_tasks = []
        list_of_projects = []
        list_of_habits = []
        list_of_tasks = []

        select_list = {
            "task": all_tasks.list_of_tasks,
            "habit": all_tasks.list_of_habits,
            "project": all_tasks.list_of_projects,
            "social_task": all_tasks.list_of_social_tasks,
        }

        for task in all_tasks:
            select_list[task.type].append(task)

        self.list_of_social_tasks = list_of_social_tasks
        self.list_of_projects = list_of_projects
        self.list_of_habits = list_of_habits
        self.list_of_tasks = list_of_tasks
