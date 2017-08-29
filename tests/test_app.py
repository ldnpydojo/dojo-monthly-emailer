import pytest
from freezegun import freeze_time

from dojo_emailer import emailer, sheet
from dojo_emailer.app import app


@pytest.fixture(autouse=True)
def mock_sheet_functions(mocker):
    mocker.patch.object(sheet, 'get_dojo_data_from_date', return_value={})
    mocker.patch.object(sheet, 'get_spreadsheet_id', return_value='')
    mocker.patch.object(sheet, 'get_first_cell_by_prefix', return_value='')


@pytest.fixture(autouse=True)
def mocked_send_email(mocker):
    mocker.patch.object(
        emailer, 'send_email', return_value={'response': 'dummy data'})


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def wrong_day():
    with freeze_time('2013-12-31'):
        yield


@pytest.fixture
def correct_day():
    with freeze_time('2017-1-24'):
        yield


def test_trigger_app_on_wrong_day(client, wrong_day):
    client.get('/')
    emailer.send_email.assert_not_called()


def test_trigger_app_on_correct_day(client, correct_day):
    client.get('/')
    emailer.send_email.assert_called()
    expected_subject = 'Monthly dojo reminder for February 2017'
    # [0] for first call, [1] to select the 2nd of (args, kwargs)
    subject = emailer.send_email.call_args_list[0][1]['subject']
    assert subject == expected_subject


def test_force_trigger_app(client, wrong_day):
    client.get('/?force=1')
    emailer.send_email.assert_called()
    expected_subject = 'Monthly dojo reminder for January 2014'
    # [0] for first call, [1] to select the 2nd of (args, kwargs)
    subject = emailer.send_email.call_args_list[0][1]['subject']
    assert subject == expected_subject
