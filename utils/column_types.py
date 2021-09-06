from enum import Enum


class ColumnTypes(Enum):
    TITLE = "title"
    ID = "id"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RELATION = "relation"
    ROLLUP = "rollup"
    DATE = "date"
    RICH_TEXT = "rich_text"
    NUMBER = "number"

