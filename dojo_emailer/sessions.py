from datetime import date, timedelta

START_YEAR = 2009
MONTHS_IN_YEAR = 12
ACADEMIC_YEAR_DIFF_MONTHS = 8
# Monday is 0 and Sunday is 6
THURSDAY = 3


def get_first_of_next_month(today):
    next_month = today.month + 1
    year, month = normalise_year_month(today.year, next_month)
    return date(year, month, 1)


def find_next_thursday(date):
    while date.weekday() != THURSDAY:
        date += timedelta(days=1)
    return date


def normalise_year_month(year, month):
    # the -1, +1 is to divmod via 0-based month count
    months_since_jesus = 12 * year + month - 1
    year, month = divmod(months_since_jesus, 12)
    return year, month + 1


def convert_episode_to_date(season, episode):
    year = START_YEAR + season - 1
    month = episode + ACADEMIC_YEAR_DIFF_MONTHS
    year, month = normalise_year_month(year, month)
    return find_next_thursday(date(year, month, 1))


def convert_date_to_episode(date_):
    season = date_.year - START_YEAR + 1
    episode = date_.month - ACADEMIC_YEAR_DIFF_MONTHS
    season, episode = normalise_year_month(season, episode)
    return season, episode
