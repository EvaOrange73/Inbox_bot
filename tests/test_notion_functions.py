from datetime import datetime, timedelta

import pytest

from notion_scripts.form_json.equals_filter import equals_filter
from notion_scripts.form_json.utils import h1, h2, h3, paragraph, bulleted_list_item, bold_paragraph, toggle
from notion_scripts.requests.add_page import add_page
from notion_scripts.requests.read_table import read_table
from notion_scripts.requests.update_page import update_page
from utils.column_types import ColumnTypes
from utils.columns import InboxColumns, ContextColumns, DiaryColumns, ReflectionColumns, DateColumns
from utils.config import inbox_table_id, context_table_id, diary_table_id, reflection_table_id, date_table_id


@pytest.mark.parametrize("table_id", [
    inbox_table_id,
    context_table_id,
    diary_table_id,
    reflection_table_id,
    date_table_id
])
def test_read_table(table_id):
    assert read_table(table_id)


@pytest.mark.parametrize("table_id, columns", [
    (inbox_table_id, InboxColumns),
    (context_table_id, ContextColumns),
    (diary_table_id, DiaryColumns),
    (reflection_table_id, ReflectionColumns),
    (date_table_id, DateColumns)
])
def test_add_page(table_id, columns):
    data = {}
    for column in columns:
        if column.column_type == ColumnTypes.TITLE.value:
            data[column] = "test page"
        elif column.column_type == ColumnTypes.DATE.value:
            data[column] = datetime.now().date().isoformat()
        elif column.column_type == ColumnTypes.CHECKBOX.value:
            data[column] = True
        elif column.column_type == ColumnTypes.RICH_TEXT.value:
            data[column] = "test text"
        elif column.column_type == ColumnTypes.SELECT.value:
            data[column] = "test select option"
        elif column.column_type == ColumnTypes.NUMBER.value:
            data[column] = 42

    assert add_page(table_id, data, "test page content")


@pytest.mark.parametrize("table_id, columns", [
    (inbox_table_id, InboxColumns),
    (context_table_id, ContextColumns),
    (diary_table_id, DiaryColumns),
    (reflection_table_id, ReflectionColumns),
    (date_table_id, DateColumns)
])
def test_update_page(table_id, columns):
    list_of_pages = read_table(table_id, filter_data=equals_filter({columns.NAME: "test page"}))

    data = {}
    for column in columns:
        if column.column_type == ColumnTypes.TITLE.value:
            data[column] = "test page2"
        elif column.column_type == ColumnTypes.DATE.value:
            data[column] = (datetime.now().date() + timedelta(days=1)).isoformat()
        elif column.column_type == ColumnTypes.CHECKBOX.value:
            data[column] = False
        elif column.column_type == ColumnTypes.RICH_TEXT.value:
            data[column] = "test text2"
        elif column.column_type == ColumnTypes.SELECT.value:
            data[column] = "test select option2"
        elif column.column_type == ColumnTypes.NUMBER.value:
            data[column] = 73

    for page in list_of_pages:
        assert update_page(page.id, data, "test page content2")


@pytest.mark.parametrize("function", [h1, h2, h3, paragraph, bulleted_list_item, bold_paragraph])
def test_add_page_content(function):
    page = read_table(inbox_table_id, filter_data=equals_filter({InboxColumns.NAME: "test page2"}))[0]
    assert update_page(page.id, data={InboxColumns.DELETE: False}, children=[function("test text")])


def test_toggle():
    page = read_table(inbox_table_id, filter_data=equals_filter({InboxColumns.NAME: "test page2"}))[0]
    assert update_page(page.id, data={}, children=[toggle("test text", [paragraph("test text")])])
