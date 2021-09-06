from enum import Enum

from utils.column_types import ColumnTypes


class Column:
    def __init__(self, title, column_type, column_subtype=""):
        self.title = title
        self.column_type = column_type
        self.column_subtype = column_subtype


class InboxColumns(Column, Enum):
    # общее
    NAME = ("Name", ColumnTypes.TITLE.value)
    ID = ("id", ColumnTypes.ID.value)
    TYPE = ("Тип", ColumnTypes.SELECT.value)
    DONE = ("Сделано", ColumnTypes.CHECKBOX.value)
    DELETE = ("Неактуально", ColumnTypes.CHECKBOX.value)
    PLANNED = ("Запланировано", ColumnTypes.CHECKBOX.value)
    PARENT = ('Родитель', ColumnTypes.RELATION.value)
    PARENT_NAME = ("Имя родителя", ColumnTypes.ROLLUP.value, ColumnTypes.TITLE.value)
    PARENT_ARCHIVE = ("Родитель: архив", ColumnTypes.RELATION.value)
    DATE = ("Дата", ColumnTypes.DATE.value)
    SPECIAL_DATE = ("Примерная дата", ColumnTypes.RELATION.value)

    TASK_TYPE = ("Тип задачи", ColumnTypes.SELECT.value)
    # задачи
    CONTEXT_TASKS = ("Контекст (для задач)", ColumnTypes.RELATION.value)
    CONTEXT_TASKS_ARCHIVE = ("Контекст (для задач): архив", ColumnTypes.RELATION.value)
    # привычки
    HABIT_START = ("Начало привычки", ColumnTypes.DATE.value)
    HABIT_SPECIAL_START = ("Примерное начало", ColumnTypes.RELATION.value)
    HABIT_END = ("Конец привычки", ColumnTypes.DATE.value)
    HABIT_SPECIAL_END = ("Примерный конец", ColumnTypes.RELATION.value)
    CONTEXT_HABITS = ("Контекст (для привычкек)", ColumnTypes.RELATION.value)
    CONTEXT_HABITS_ARCHIVE = ("Контекст (для привычкек): архив", ColumnTypes.RELATION.value)
    # проекты
    CHILD = ('Ребёнок', ColumnTypes.RELATION.value)
    CHILD_ARCHIVE = ('Ребёнок: архив', ColumnTypes.RELATION.value)
    CONTEXT_PROJECTS = ("Контекст (для поектов)", ColumnTypes.RELATION.value)
    CONTEXT_PROJECTS_ARCHIVE = ("Контекст (для поектов): архив", ColumnTypes.RELATION.value)
    # задачи, требующие общения
    DESCRIPTION = ("Описание", ColumnTypes.RICH_TEXT.value)
    NEXT_STEP = ("Следующий шаг", ColumnTypes.SELECT.value)
    CONTEXT_SOCIALS = ("Контекст (требуют общения)", ColumnTypes.RELATION.value)
    CONTEXT_SOCIALS_ARCHIVE = ("Контекст (требуют общения): архив", ColumnTypes.RELATION.value)


class ContextColumns(Column, Enum):
    NAME = ("Name", ColumnTypes.TITLE.value)
    ID = ("id", ColumnTypes.ID.value)
    DELETE = ("Неактуально", ColumnTypes.CHECKBOX.value)
    HANGOUT = ("Туса", ColumnTypes.CHECKBOX.value)
    CONDITIONS = ("Условия", ColumnTypes.RICH_TEXT.value)
    RESULT = ("Результат", ColumnTypes.RICH_TEXT.value)
    DESCRIPTION = ("Описание", ColumnTypes.CHECKBOX.value)
    TASKS = ("Задачи", ColumnTypes.RELATION.value)
    TASKS_ARCHIVE = ("Задачи: архив", ColumnTypes.RELATION.value)
    PROJECTS = ("Проекты", ColumnTypes.RELATION.value)
    PROJECTS_ARCHIVE = ("Проекты: архив", ColumnTypes.RELATION.value)
    SOCIALS = ("Требуют общения", ColumnTypes.RELATION.value)
    SOCIALS_ARCHIVE = ("Требуют общения: архив", ColumnTypes.RELATION.value)
    HABITS = ("Привычки", ColumnTypes.RELATION.value)
    HABITS_ARCHIVE = ("Привычки: архив", ColumnTypes.RELATION.value)
    SUM = ("Сумма", ColumnTypes.NUMBER.value)


class DiaryColumns(Column, Enum):
    NAME = ("Name", ColumnTypes.TITLE.value)
    ID = ("id", ColumnTypes.ID.value)
    DATE = ("Дата", ColumnTypes.DATE.value)
    CONTEXTS = ("Контексты", ColumnTypes.RELATION.value)
    HANGOUTS = ("Тусы", ColumnTypes.ROLLUP.value, ColumnTypes.CHECKBOX.value)
    REFLECTION = ("Рефлексия", ColumnTypes.RELATION.value)
    CONTEXT_NAMES = ("имя контекста", ColumnTypes.ROLLUP.value, ColumnTypes.TITLE.value)


class DateColumns(Column, Enum):
    NAME = ("Name", ColumnTypes.TITLE.value)
    ID = ("id", ColumnTypes.ID.value)
    DATE = ("Дата", ColumnTypes.DATE.value)
    IS_EXACT = ("Точно", ColumnTypes.CHECKBOX.value)


class ReflectionColumns(Column, Enum):
    NAME = ("Name", ColumnTypes.TITLE.value)
    ID = ("id", ColumnTypes.ID.value)
    DATE = ("Дата", ColumnTypes.DATE.value)
    TYPE = ("Тип", ColumnTypes.SELECT.value)
    PRODUCTIVITY = ("Продуктивность", ColumnTypes.RICH_TEXT.value)
    HANGOUTS = ("Тусы", ColumnTypes.RICH_TEXT.value)
    IS_PROCESSED = ("Обработано", ColumnTypes.CHECKBOX.value)
    PARENT = ('Родитель', ColumnTypes.RELATION.value)
    CHILD = ('Ребёнок', ColumnTypes.RELATION.value)
    DAY_TASKS = ("Задачи на день", ColumnTypes.RELATION.value)
