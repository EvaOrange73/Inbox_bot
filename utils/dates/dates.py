from datetime import datetime, timedelta

from dto.item import Item
from dto.update_date import UpdateDate
from notion_scripts.requests.read_table import read_table
from utils.columns import InboxColumns
from utils.config import date_table_id

key_words = [UpdateDate("сегодня", datetime.now().date().isoformat(), InboxColumns.DATE),
             UpdateDate("завтра", (datetime.now().date() + timedelta(days=1)).isoformat(), InboxColumns.DATE),
             UpdateDate("послезавтра", (datetime.now().date() + timedelta(days=2)).isoformat(), InboxColumns.DATE)
             ]


def get_dates_for_keyboard():
    dates_for_keyboard = []
    for key_word in key_words:
        dates_for_keyboard.append(key_word.name)
    special_dates = read_table(date_table_id)
    for date in special_dates:
        dates_for_keyboard.append(date.name)
    return dates_for_keyboard


def get_only_special_dates_for_keyboard():
    only_special_dates_for_keyboard = []
    special_dates = read_table(date_table_id)
    for date in special_dates:
        only_special_dates_for_keyboard.append(Item(date.name, date.date))
    return only_special_dates_for_keyboard
