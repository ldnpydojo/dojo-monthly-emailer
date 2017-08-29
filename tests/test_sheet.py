"Integration tests. Makes actual calls to Google Spreadsheets API."
import re
from datetime import date

from dojo_emailer.app import (
    GDOCS_URL_PREFIX,
    GDOCS_URL_SHEET_NAME,
    SPREADSHEET_NAME
)
from dojo_emailer.sheet import (
    get_dojo_data_from_date,
    get_first_cell_by_prefix,
    get_spreadsheet_id
)


def test_get_spreadsheet_id():
    # check start and end of id without divulging entire value here
    expected_id_regex = r'18yYx.{34}q39DM'
    spreadsheet_id = get_spreadsheet_id(SPREADSHEET_NAME)
    assert re.match(expected_id_regex, spreadsheet_id)


def test_get_first_cell_by_prefix():
    expected_url_regex = \
        r'https://docs.google.com/document/d/1WyDe.{34}Z0z9s/.*'
    url = get_first_cell_by_prefix(
        SPREADSHEET_NAME, GDOCS_URL_SHEET_NAME, GDOCS_URL_PREFIX)
    assert re.match(expected_url_regex, url)


def test_get_first_cell_by_prefix_with_missing_prefix():
    sheet_not_containing_a_gdocs_url = 'Email Addresses'
    url = get_first_cell_by_prefix(
        SPREADSHEET_NAME, sheet_not_containing_a_gdocs_url, GDOCS_URL_PREFIX)
    assert url is None


def test_get_dojo_data_from_date():
    expected_data = {
        'S': 8,
        'E': 5,
        'Cat-Herder': 'Tom',
        'Day': 'Thursday 5th January',
        'Month': 'January 2017',
        'Person on the Inside': 'Marcus',
        'Venue': 'SohoNet',
    }
    date_ = date(2017, 1, 1)
    data = get_dojo_data_from_date(SPREADSHEET_NAME, date_)
    for key, expected_value in expected_data.items():
        assert data[key] == expected_value
