from datetime import datetime, timedelta

# months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
# "Декабрь"]
from dto.update_date import UpdateDate
from utils.columns import InboxColumns

# Поддерживаемые форматы даты:
# сегодня, завтра
# на этой неделе, потом
# любая дата из таблицы "примерные даты"
# в понедельник
# 5 вгуста
# 2.03.2021
from utils.dates.dates import key_words, special_dates

months_short = ["ян", "фе", "мар", "ап", "ма", "июн", "июл", "ав", "се", "ок", "но", "де"]
weekdays_short = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
weekdays_long = ["по", "вт", "ср", "че", "пя", "су", "во"]


def parse_date(text):
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

            if date_list[1][2].lower() in ['р', 'н', 'л']:
                month_short = date_list[1][:3].lower()
            else:
                month_short = date_list[1][:2].lower()

            month = months_short.index(month_short) + 1

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
