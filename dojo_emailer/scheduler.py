from datetime import timedelta

# Monday is 0 and Sunday is 6
THURSDAY = 3
# 1-based (unlike Javascript)
AUGUST = 8
DAYS_IN_WEEK = 7


def is_reminder_day(day):
    """Tuesday before the last Thursday before the first Thursday.

    Except August.
    Logic written in terms of the possible dojo day.
    """
    # 2nd thursday after `day`
    possible_dojo = day + timedelta(days=9)
    is_thurs = possible_dojo.weekday() == THURSDAY
    is_august = possible_dojo.month == AUGUST
    is_first_week_of_month = possible_dojo.day <= DAYS_IN_WEEK
    return is_thurs and is_first_week_of_month and not is_august
