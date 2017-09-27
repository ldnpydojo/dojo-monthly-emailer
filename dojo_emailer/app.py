from datetime import date

from flask import Flask, jsonify, render_template, request
from logzero import logger

# importing like this allows mocking e.g. sheet.<name>
from dojo_emailer import emailer, sheet
from dojo_emailer.scheduler import is_reminder_day
from dojo_emailer.sessions import get_first_of_next_month

# email settings
FROM_ADDRESS = 'Dojo monthly reminder <reminder@ldnpydojo.org.uk>'
TO_ADDRESS = 'Dojo discuss <discuss@ldnpydojo.org.uk>'
TO_ADDRESS = FROM_ADDRESS
SUBJECT = 'Monthly dojo reminder for {0:%B} {0:%Y}'
TEMPLATE_FILENAME = 'reminder_template.html'

# google spreadsheet settings
SPREADSHEET_NAME = "Dojo sessions"
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/{id}'
# to keep the url of our google doc private, we read it from this sheet
GDOCS_URL_SHEET_NAME = 'Eventbrite Steps'
GDOCS_URL_PREFIX = 'https://docs.google.com/document'

app = Flask(__name__)


@app.route('/')
def send_email_endpoint():
    """Sends a reminder email if today is a reminder day.

    Add ?force=1 to send a test email regardless of date.
    """
    today = date.today()
    today_is_reminder_day = is_reminder_day(today)
    force_send = request.args.get('force') == '1'
    email_sent = today_is_reminder_day or force_send
    first_of_next_month = get_first_of_next_month(today)
    spreadsheet_id = sheet.get_spreadsheet_id(SPREADSHEET_NAME)
    context = {
        'next_dojo_data': sheet.get_dojo_data_from_date(
            SPREADSHEET_NAME, first_of_next_month),
        'spreadsheet_url': SPREADSHEET_URL.format(id=spreadsheet_id),
        'doc_url': sheet.get_first_cell_by_prefix(
            SPREADSHEET_NAME, GDOCS_URL_SHEET_NAME, GDOCS_URL_PREFIX),
    }
    html = render_template(TEMPLATE_FILENAME, **context)
    response = None
    if email_sent:
        response = emailer.send_email(
            from_address=FROM_ADDRESS,
            to_address=TO_ADDRESS,
            subject=SUBJECT.format(first_of_next_month),
            message_html=html)
    logging_data = {
        "today": today,
        "today_is_reminder_day": today_is_reminder_day,
        "force_send": force_send,
        "email_sent": email_sent,
        "email_context": context,
        "send_email_response": response,
        "email_html": html,
        'query_args': request.args,
    }
    logger.info(logging_data)
    return jsonify(logging_data)
