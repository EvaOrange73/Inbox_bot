from enum import Enum

weekday = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


class InboxProperties(Enum):
    TASK = 'задача'
    INFO = 'инфа'
    TODAY = 'сегодня'
    TOMORROW = "завтра"
    HABIT = "привычка"
    PROJECT = "проект"
    SINGLE_TASK = "одно действие"
    SOCIAL_TASK = "требует общения"


class ContextProperties(Enum):
    TIME_MORNING = "утро"


class ReflectionProperties(Enum):
    DAY = "День"
    SMALL_PERIOD = "Небольшой период (5-10 дней)"
    IMPORTANT_PERIOD = "Значимый период"
