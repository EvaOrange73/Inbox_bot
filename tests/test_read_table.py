import pytest

from notion_scripts.requests.read_table import read_table
from utils.config import inbox_table_id, context_table_id, diary_table_id, reflection_table_id, date_table_id


@pytest.mark.parametrize("table_id",
                         [inbox_table_id, context_table_id, diary_table_id, reflection_table_id, date_table_id])
def test_read_table(table_id):
    assert read_table(table_id)
