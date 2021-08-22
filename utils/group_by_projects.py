class Project:
    def __init__(self, name, list_of_tasks):
        self.list_of_tasks = list_of_tasks
        self.name = name


def group_by_projects(list_of_tasks):
    list_of_project_names = [""]
    list_of_projects = []
    for task in list_of_tasks:
        if not (task.parent_name in list_of_project_names):
            list_of_project_names.append(task.parent_name)
    for project_name in list_of_project_names:
        project = Project(project_name, [])
        for task in list_of_tasks:
            if task.parent_name == project_name:
                project.list_of_tasks.append(task)
        list_of_projects.append(project)

    return list_of_projects
