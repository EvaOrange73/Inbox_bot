from enum import Enum


class Column:
    def __init__(self, title, column_type):
        self.title = title
        self.column_type = column_type


class InboxColumns(Column, Enum):
    # общее
    NAME = ("Name", "title")
    TYPE = ("Тип", "select")
    DONE = ("Сделано", "checkbox")
    DELETE = ("Неактуально", "checkbox")
    PLANNED = ("Запланировано", "checkbox")
    PARENT = ('Родитель', "relation")
    PARENT_ARCHIVE = ("Родитель: архив", "relation")
    DATE = ("Дата", "date")
    SPECIAL_DATE = ("Примерная дата", "relation")
    # задачи
    CONTEXT_TASKS = ("Контекст (для задач)", "relation")
    CONTEXT_TASKS_ARCHIVE = ("Контекст (для задач): архив", "relation")
    # привычки
    HABIT = ("Привычка", "checkbox")
    HABIT_START = ("Начало привычки", "date")
    HABIT_SPECIAL_START = ("Примерное начало", "relation")
    HABIT_END = ("Конец привычки", "date")
    HABIT_SPECIAL_END = ("Примерный конец", "relation")
    CONTEXT_HABITS = ("Контекст (для привычкек)", "relation")
    CONTEXT_HABITS_ARCHIVE = ("Контекст (для привычкек): архив", "relation")
    # проекты
    PROJECT = ("Проект", "checkbox")
    CHILD = ('Ребёнок', "relation")
    CHILD_ARCHIVE = ('Ребёнок: архив', "relation")
    CONTEXT_PROJECTS = ("Контекст (для поектов)", "relation")
    CONTEXT_PROJECTS_ARCHIVE = ("Контекст (для поектов): архив", "relation")
    # задачи, требующие общения
    SOCIAL = ("Требует общения", "checkbox")
    DESCRIPTION = ("Описание", "rich_text")
    NEXT_STEP = ("Следующий шаг", "select")
    CONTEXT_SOCIALS = ("Контекст (требуют общения)", "relation")
    CONTEXT_SOCIALS_ARCHIVE = ("Контекст (требуют общения): архив", "relation")


class ContextColumns(Column, Enum):
    NAME = ("Name", "title")
    DELETE = ("Неактуально", "checkbox")
    CONDITIONS = ("Условия", "rich_text")
    RESULT = ("Результат", "rich_text")
    DESCRIPTION = ("Описание", "checkbox")
    TASKS = ("Задачи", "relation")
    TASKS_ARCHIVE = ("Задачи: архив", "relation")
    PROJECTS = ("Проекты", "relation")
    PROJECTS_ARCHIVE = ("Проекты: архив", "relation")
    SOCIALS = ("Требуют общения", "relation")
    SOCIALS_ARCHIVE = ("Требуют общения: архив", "relation")
    HABITS = ("Привычки", "relation")
    HABITS_ARCHIVE = ("Привычки: архив", "relation")


class DiaryColumns(Column, Enum):
    NAME = ("Name", "title")
    DATE = ("Дата", "date")
    CONTEXTS = ("Контексты", "relation")


class DateColumns(Column, Enum):
    NAME = ("Name", "title")
    DATE = ("Дата", "date")
    IS_EXACT = ("Точно", "checkbox")


class ReflectionColumns(Column, Enum):
    NAME = ("Name", "title")
    DATE = ("Дата", "date")
    TYPE = ("Тип", "select")
    PRODUCTIVITY = ("Продуктивность", "rich_text")
    HANGOUTS = ("Тусовки", "rich_text")
    IS_PROCESSED = ("Обработано", "checkbox")
    PARENT = ('Родитель', "relation")
    CHILD = ('Ребёнок', "relation")
