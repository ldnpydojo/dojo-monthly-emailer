import boto3
import pytest
from moto import mock_ses

from dojo_emailer.emailer import send_email


@pytest.fixture
def ses_conn(monkeypatch):
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'eu-west-1')
    with mock_ses():
        yield boto3.client('ses')


@pytest.fixture
def verified_address(ses_conn):
    address = "test@example.com"
    ses_conn.verify_email_identity(EmailAddress=address)
    return address


def test_send_email(verified_address, ses_conn):
    send_email(
        from_address=verified_address,
        to_address=verified_address,
        subject='test subject',
        message_html='<b>hi</b>')
    send_quota = ses_conn.get_send_quota()
    sent_count = int(send_quota['SentLast24Hours'])
    assert sent_count == 1
