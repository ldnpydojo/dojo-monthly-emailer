from datetime import date

import pytest

from dojo_emailer.sessions import (
    convert_date_to_episode,
    convert_episode_to_date
)

test_data = (
    (1, 1, date(2009, 9, 3)),
    (4, 1, date(2012, 9, 6)),
    (4, 2, date(2012, 10, 4)),
    (4, 4, date(2012, 12, 6)),
    (4, 5, date(2013, 1, 3)),
    (4, 10, date(2013, 6, 6)),
    (4, 11, date(2013, 7, 4)),
    (10, 1, date(2018, 9, 6)),
    (10, 11, date(2019, 7, 4)),
    # if we ever cancel holidays, ep12 will be in August
    (10, 12, date(2019, 8, 1)),
)


@pytest.mark.parametrize('season, episode, expected_date', test_data)
def test_convert_episode_to_date(season, episode, expected_date):
    assert convert_episode_to_date(season, episode) == expected_date


@pytest.mark.parametrize('expected_season, expected_episode, date_', test_data)
def test_convert_date_to_episode(expected_season, expected_episode, date_):
    assert convert_date_to_episode(date_) == (
        expected_season, expected_episode)
