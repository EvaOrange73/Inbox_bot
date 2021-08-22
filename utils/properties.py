from enum import Enum


class InboxProperties(Enum):
    TASK = 'задача'
    INFO = 'инфа'
    TODAY = 'сегодня'
    TOMORROW = "завтра"


class ContextProperties(Enum):
    TIME_MORNING = "утро"
