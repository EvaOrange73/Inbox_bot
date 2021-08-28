from dto.reflection import Reflection
from notion_scripts.parse_json.parse_column import parse_column
from utils.columns import ReflectionColumns


def make_reflection(data):

    return Reflection(
        id=parse_column(data, ReflectionColumns.ID),
        name=parse_column(data, ReflectionColumns.NAME),
        type=parse_column(data, ReflectionColumns.TYPE),
        date=parse_column(data, ReflectionColumns.DATE),
        productivity=parse_column(data, ReflectionColumns.PRODUCTIVITY),
        hangouts=parse_column(data, ReflectionColumns.HANGOUTS),
        is_processed=parse_column(data, ReflectionColumns.IS_PROCESSED)
    )
