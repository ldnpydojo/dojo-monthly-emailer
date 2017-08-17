import json
import os
from collections import OrderedDict

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dojo_emailer.sessions import convert_date_to_episode

AUTH_ENV_VAR = 'DOJO_GAUTH_JSON'


def gsheets_api_connect():
    scope = ['https://spreadsheets.google.com/feeds']
    gauth_json = os.environ[AUTH_ENV_VAR]
    gauth_dict = json.loads(gauth_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        gauth_dict, scope)
    return gspread.authorize(credentials)


def get_first_cell_by_prefix(spreadsheet_name, sheet_name, prefix):
    """Reads contents of a sheet, and returns the first doc link found.

    If none is found, returns None.
    """
    conn = gsheets_api_connect()
    spreadsheet = conn.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(sheet_name)
    rows = sheet.get_all_values()
    for row in rows:
        for cell in row:
            if cell.startswith(prefix):
                return cell
    return None


def get_spreadsheet_id(spreadsheet_name):
    conn = gsheets_api_connect()
    spreadsheet = conn.open(spreadsheet_name)
    return spreadsheet.id


def get_dojo_spreadsheet_data(spreadsheet_name):
    conn = gsheets_api_connect()
    spreadsheet = conn.open(spreadsheet_name)
    data = spreadsheet.sheet1.get_all_records()
    headers = spreadsheet.sheet1.row_values(1)

    episode2row = OrderedDict()
    for row in data:
        try:
            season = int(row['S'])
            episode = int(row['E'])
        except ValueError:
            continue

        def hdr_order(key_value):
            key, _ = key_value
            return headers.index(key)

        ordered_row_data = OrderedDict(sorted(row.items(), key=hdr_order))
        episode2row[(season, episode)] = ordered_row_data
    return episode2row


def get_dojo_row_data(spreadsheet_name, season, episode):
    data = get_dojo_spreadsheet_data(spreadsheet_name)
    return data[(season, episode)]


def get_dojo_data_from_date(spreadsheet_name, date):
    season, episode = convert_date_to_episode(date)
    return get_dojo_row_data(spreadsheet_name, season, episode)
