from handlers.working.get_social_tasks import get_social_tasks
from notion_scripts.form_json.utils import bulleted_list_item, h3, h2, paragraph, bold_paragraph
from utils.group_by_projects import group_by_projects


def form_day_content(list_of_context, list_of_social_tasks):
    children = [paragraph(get_social_tasks(list_of_social_tasks))]
    for context in list_of_context:
        children.append(h2(context.text))
        children.append(h3("Условия:"))
        children.append(paragraph(context.start))
        if len(context.habits):
            children.append(h3("Привычки:"))
            for habit in context.habits:
                children.append(bulleted_list_item(habit.text))
        if len(context.all_tasks):
            children.append(h3("Задачи:"))
            for project in group_by_projects(context.all_tasks):
                if project.name != "":
                    children.append(bold_paragraph(project.name))
                for task in project.list_of_tasks:
                    children.append(bulleted_list_item(task.text))
        children.append(h3("Результат:"))
        children.append(paragraph(context.end))

    return children
