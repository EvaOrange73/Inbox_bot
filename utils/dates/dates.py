from datetime import datetime, timedelta

from dto.update_date import UpdateDate
from notion_scripts.requests.read_special_dates import read_special_dates
from utils.columns import InboxColumns

dates_for_keyboard = []

key_words = {
    "сегодня": UpdateDate(datetime.now().date().isoformat(), InboxColumns.DATE),
    "завтра": UpdateDate((datetime.now().date() + timedelta(days=1)).isoformat(), InboxColumns.DATE),
    "послезавтра": UpdateDate((datetime.now().date() + timedelta(days=2)).isoformat(), InboxColumns.DATE)
}
for key_word in key_words.keys():
    dates_for_keyboard.append(key_word)

special_dates = read_special_dates()
for date in special_dates.keys():
    dates_for_keyboard.append(date)
