from datetime import datetime, timedelta

from dto.item import Item
from dto.update_date import UpdateDate
from notion_scripts.requests.read_special_dates import read_special_dates
from utils.columns import InboxColumns

key_words = {
    "сегодня": UpdateDate(datetime.now().date().isoformat(), InboxColumns.DATE),
    "завтра": UpdateDate((datetime.now().date() + timedelta(days=1)).isoformat(), InboxColumns.DATE),
    "послезавтра": UpdateDate((datetime.now().date() + timedelta(days=2)).isoformat(), InboxColumns.DATE)
}


def get_dates_for_keyboard():
    dates_for_keyboard = []
    for key_word in key_words.keys():
        dates_for_keyboard.append(key_word)
    special_dates = read_special_dates()
    for date in special_dates.keys():
        dates_for_keyboard.append(date)
    return dates_for_keyboard


def get_only_special_dates_for_keyboard():
    only_special_dates_for_keyboard = []
    special_dates = read_special_dates()
    for date in special_dates.keys():
        only_special_dates_for_keyboard.append(Item(date, special_dates[date].date))
    return only_special_dates_for_keyboard
