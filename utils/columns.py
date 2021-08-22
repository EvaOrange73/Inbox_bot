from enum import Enum


class Column:
    def __init__(self, title, column_type):
        self.title = title
        self.column_type = column_type


class InboxColumns(Column, Enum):
    NAME = ("Name", "title")
    TYPE = ("Тип", "select")
    DONE = ("Сделано", "checkbox")
    DELETE = ("Неактуально", "checkbox")
    PROJECT = ("Проект", "checkbox")
    HABIT = ("Привычка", "checkbox")
    SOCIAL = ("Требует общения", "checkbox")
    PLANNED = ("Запланировано", "checkbox")
    DESCRIPTION = ("Описание", "rich_text")
    NEXT_STEP = ("Следующий шаг", "select")
    WHEN = ("Когда?", "select")
    HABIT_START = ("Начало привычки", "date")
    HABIT_END = ("Конец привычки", "date")
    PARENT = ('Родитель', "relation")
    CHILD = ('Ребёнок', "relation")
    CONTEXT_TASKS = ("Контекст (для задач)", "relation")
    CONTEXT_PROJECTS = ("Контекст (для поектов)", "relation")
    CONTEXT_SOCIALS = ("Контекст (требуют общения)", "relation")
    CONTEXT_HABITS = ("Контекст (для привычкек)", "relation")
    DATE = ("Дата", "date")


class ContextColumns(Column, Enum):
    NAME = ("Name", "title")
    DELETE = ("Неактуально", "checkbox")
    CONDITIONS = ("Условия", "rich_text")
    RESULT = ("Результат", "rich_text")
    TIME = ("Время", "select")
    DESCRIPTION = ("Описание", "checkbox")
    TASKS = ("Задачи", "relation")
    PROJECTS = ("Проекты", "relation")
    SOCIALS = ("Требуют общения", "relation")
    HABITS = ("Привычки", "relation")


class DiaryColumns(Column, Enum):
    NAME = ("Name", "title")
    DATE = ("Дата", "date")
    CONTEXTS = ("Контексты", "relation")


class DateColumns(Column, Enum):
    NAME = ("Name", "title")
    DATE = ("Дата", "date")
