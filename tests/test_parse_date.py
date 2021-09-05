import pytest

from utils.dates.parse_date import parse_date


@pytest.mark.parametrize("string", [
    "сегодня",
    "завтра",
    "5 мая",
    "8 февраля 2022",
    "в понедельник",
    "во вторник"
    "2.03.2021",
    "потом",
    "в следующуюю среду"
])
def test_parse_date(string):
    assert parse_date(string)
    print(parse_date(string).date)
