from enum import Enum


class Column:
    def __init__(self, title, column_type, column_subtype=""):
        self.title = title
        self.column_type = column_type
        self.column_subtype = column_subtype


class InboxColumns(Column, Enum):
    # общее
    NAME = ("Name", "title")
    ID = ("id", "id")
    TYPE = ("Тип", "select")
    DONE = ("Сделано", "checkbox")
    DELETE = ("Неактуально", "checkbox")
    PLANNED = ("Запланировано", "checkbox")
    PARENT = ('Родитель', "relation")
    PARENT_NAME = ("Имя родителя", "rollup", "title")
    PARENT_ARCHIVE = ("Родитель: архив", "relation")
    DATE = ("Дата", "date")
    SPECIAL_DATE = ("Примерная дата", "relation")

    TASK_TYPE = ("Тип задачи", "select")
    # задачи
    CONTEXT_TASKS = ("Контекст (для задач)", "relation")
    CONTEXT_TASKS_ARCHIVE = ("Контекст (для задач): архив", "relation")
    # привычки
    HABIT_START = ("Начало привычки", "date")
    HABIT_SPECIAL_START = ("Примерное начало", "relation")
    HABIT_END = ("Конец привычки", "date")
    HABIT_SPECIAL_END = ("Примерный конец", "relation")
    CONTEXT_HABITS = ("Контекст (для привычкек)", "relation")
    CONTEXT_HABITS_ARCHIVE = ("Контекст (для привычкек): архив", "relation")
    # проекты
    CHILD = ('Ребёнок', "relation")
    CHILD_ARCHIVE = ('Ребёнок: архив', "relation")
    CONTEXT_PROJECTS = ("Контекст (для поектов)", "relation")
    CONTEXT_PROJECTS_ARCHIVE = ("Контекст (для поектов): архив", "relation")
    # задачи, требующие общения
    DESCRIPTION = ("Описание", "rich_text")
    NEXT_STEP = ("Следующий шаг", "select")
    CONTEXT_SOCIALS = ("Контекст (требуют общения)", "relation")
    CONTEXT_SOCIALS_ARCHIVE = ("Контекст (требуют общения): архив", "relation")


class ContextColumns(Column, Enum):
    NAME = ("Name", "title")
    ID = ("id", "id")
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
    ID = ("id", "id")
    DATE = ("Дата", "date")
    CONTEXTS = ("Контексты", "relation")
    HANGOUTS = ("Тусы", "rollup", "checkbox")
    REFLECTION = ("Рефлексия", "relation")
    CONTEXT_NAMES = ("имя контекста", "rollup", "title")


class DateColumns(Column, Enum):
    NAME = ("Name", "title")
    ID = ("id", "id")
    DATE = ("Дата", "date")
    IS_EXACT = ("Точно", "checkbox")


class ReflectionColumns(Column, Enum):
    NAME = ("Name", "title")
    ID = ("id", "id")
    DATE = ("Дата", "date")
    TYPE = ("Тип", "select")
    PRODUCTIVITY = ("Продуктивность", "rich_text")
    HANGOUTS = ("Тусы", "rich_text")
    IS_PROCESSED = ("Обработано", "checkbox")
    PARENT = ('Родитель', "relation")
    CHILD = ('Ребёнок', "relation")
    DAY_TASKS = ("Задачи на день", "relation")
