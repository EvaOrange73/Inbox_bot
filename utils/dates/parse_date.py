from datetime import datetime, timedelta

# months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
# "Декабрь"]
from dto.update_date import UpdateDate
from notion_scripts.requests.read_special_dates import read_special_dates
from utils.columns import InboxColumns
# Поддерживаемые форматы даты:
# сегодня, завтра
# на этой неделе, потом
# любая дата из таблицы "примерные даты"
# в понедельник
# 5 вгуста
# 2.03.2021
from utils.dates.dates import key_words

months_short = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
weekdays_short = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
weekdays_long = ["по", "вт", "ср", "че", "пя", "су", "во"]
special_dates = read_special_dates()


def parse_date(text):
    try:
        if key_words.get(text) is not None:
            return key_words.get(text)
        elif special_dates.get(text) is not None:
            return special_dates.get(text)
        elif text[0].isdigit():
            if text.find(".") != -1:
                date = datetime.strptime(text, "%d.%m.%Y").date()
                return UpdateDate(date, InboxColumns.DATE)
            else:
                date_list = list(text.split(" "))
                day = int(date_list[0])

                month = months_short.index(date_list[1][:3].lower()) + 1

                if len(date_list) == 3:
                    year = int(date_list[2])
                else:
                    year = datetime.now().year
                    if datetime.now().month > month:
                        year += 1

                return UpdateDate(datetime(year, month, day).date().isoformat(), InboxColumns.DATE)
        else:
            weekday = list(text.split(" "))[-1]
            try:
                weekday = weekdays_short.index(weekday[:2])
            except ValueError:
                weekday = weekdays_long.index(weekday[:2])

            date = datetime.now().date() + timedelta(days=1)
            while date.weekday() != weekday:
                date += timedelta(days=1)

            return UpdateDate(date.isoformat(), InboxColumns.DATE)
    except:
        return None
