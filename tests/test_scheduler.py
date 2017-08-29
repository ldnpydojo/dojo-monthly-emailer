from datetime import date, timedelta

import pytest

from dojo_emailer.scheduler import is_reminder_day

# Monday is 0 and Sunday is 6
TUESDAY = 1
# 1-based (unlike Javascript)
JULY = 7

DAYS_IN_2017 = 365

# Manually written list of reminder dates in 2017
remind_dates_2017 = (
    date(2017, 1, 24),
    date(2017, 2, 21),
    date(2017, 3, 28),
    date(2017, 4, 25),
    date(2017, 5, 23),
    date(2017, 6, 27),
    date(2017, 8, 29),
    date(2017, 9, 26),
    date(2017, 10, 24),
    date(2017, 11, 28),
    date(2017, 12, 26),
)

jan_1st = date(2017, 1, 1)
year_days = [jan_1st + timedelta(days=i) for i in range(DAYS_IN_2017)]
test_data = [(day, day in remind_dates_2017) for day in year_days]


@pytest.mark.parametrize('day, expect_send', test_data)
def test_sanity_check_test_data(day, expect_send):
    """Tuesday before the last Thursday, excluding August dojo."""
    # Let's write this logic in terms of the reminder day.
    is_tuesday = day.weekday() == TUESDAY
    tue_before_last_thurs = (
        (day + timedelta(days=2)).month !=
        (day + timedelta(days=9)).month
    )
    is_july = day.month == JULY
    # sanity check our manually written test data
    assert (
        is_tuesday and tue_before_last_thurs and not is_july
    ) == expect_send


@pytest.mark.parametrize('day, expect_send', test_data)
def test_is_reminder_day(day, expect_send):
    assert is_reminder_day(day) == expect_send
