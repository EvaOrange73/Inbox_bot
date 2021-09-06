from datetime import datetime, timedelta

# months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
# "Декабрь"]
from dto.update_date import UpdateDate
from notion_scripts.requests.read_table import read_table
from utils.columns import InboxColumns
from utils.config import date_table_id
from utils.dates.dates import key_words

months_short = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
weekdays_short = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
weekdays_long = ["по", "вт", "ср", "че", "пя", "су", "во"]
special_dates = read_table(date_table_id)


def parse_date(text):
    try:
        for key_word in key_words:
            if key_word.name == text:
                return key_word
        for date in special_dates:
            if date.name == text:
                return date
        if text[0].isdigit():
            if text.find(".") != -1:
                date = datetime.strptime(text, "%d.%m.%Y").date()
                return UpdateDate(name=text, date=date, column=InboxColumns.DATE)

            date_list = list(text.split(" "))
            day = int(date_list[0])

            month = months_short.index(date_list[1][:3].lower()) + 1

            if len(date_list) == 3:
                year = int(date_list[2])
            else:
                year = datetime.now().year
                if datetime.now().month > month:
                    year += 1

            return UpdateDate(name=text, date=datetime(year, month, day).date().isoformat(), column=InboxColumns.DATE)

        weekday = list(text.split(" "))[-1]
        try:
            weekday = weekdays_short.index(weekday[:2])
        except ValueError:
            weekday = weekdays_long.index(weekday[:2])

        date = datetime.now().date() + timedelta(days=1)
        while date.weekday() != weekday:
            date += timedelta(days=1)

        return UpdateDate(name=text, date=date.isoformat(), column=InboxColumns.DATE)
    except ValueError:
        return None
