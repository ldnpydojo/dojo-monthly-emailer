# dojo-monthly-emailer

_the little bird that spurred the cat herd_

[![Build Status](https://travis-ci.org/tomviner/dojo-monthly-emailer.svg?branch=master)](https://travis-ci.org/tomviner/dojo-monthly-emailer) [![Coverage Status](https://coveralls.io/repos/github/tomviner/dojo-monthly-emailer/badge.svg?branch=master)](https://coveralls.io/github/tomviner/dojo-monthly-emailer?branch=master) [![codecov](https://codecov.io/gh/tomviner/dojo-monthly-emailer/branch/master/graph/badge.svg)](https://codecov.io/gh/tomviner/dojo-monthly-emailer)

## How it works

[zappa](https://github.com/Miserlou/Zappa) is a Python library that facilitates serverless web apps on AWS lambda.

We use zappa to set up an AWS lambda function accessable via an API Gateway URL. The function sends a reminder email anytime it's called on a Tuesday before the last Thursday of the month.

This is triggered by an [IFTTT](https://ifttt.com/) applet once a day:

![If every day at 09:00 AM, then make a web request](https://i.imgur.com/2f8IBvu.png)

We use [`pynt`](https://rags.github.io/pynt/) for a few "build" commands. Run `pynt -l` (and read `build.py)` to see available commands. You'll need to: `pip install .[build]`.


## Manual testing

The API Gateway URL, can also be used for manual testing. Running a deploy/update will notify you of this URL, and we can store it in the dojo organiser spreadsheet for reference.

Add `?force=1` to send a reminder email regardless of date.


## Manual steps for deploying on a new AWS account

- [zappa](https://github.com/Miserlou/Zappa) copies Python requirements directly from the active virtualenv
- so make an env, but note any random stuff you also install, gets uploaded too!
    - `mkvirtualenv dojo-emailer`

- install code and requirements
    - `pip install -e .`

- you may also like to install the test & build reqs via:
    - `pip install .[test,build]`

- setup local AWS credentials, perhaps with
    - `pip install awscli`
    - `aws configure`

- add discuss@ldnpydojo-org-uk as an AWS SES verified email
    - https://eu-west-1.console.aws.amazon.com/ses/home?region=eu-west-1#verified-senders-email:

- local folders, even if git ignored, can make the zappa package file larger, so clean up first:
    - `pynt clean`

- do a zappa deploy of the lambda function
    - `zappa deploy dev`


## Updating deployment

- if you have already deployed once, do a zappa update of the lambda function
    - `zappa update dev`


## Access to the Google Spreadsheet

Steps to setup the access:
- [Obtain OAuth2 credentials from Google Developers Console](http://gspread.readthedocs.io/en/latest/oauth2.html)
- create a _Service Account Key_ you should end up with a json file containing the credentials including a private key, so keep this file private
- you must give your Google dev account access to the spreadsheet
    - browse to the spreadsheet and share it to the `client_email` listed in the json credentials file
- to run tests or run the Flask app locally, you'll need to export these credentials to an env var:
    - e.g. `export DOJO_GAUTH_JSON="$(cat 'Dojo-monthly-emailer-0ea2b2dfe580.json')"`
- when setting up a new travis-ci test runner, you'll also need to set this env var, and because it's injected unescaped into the shell, you must wrap the json value with single quotes
- the AWS lambda function also needs this value. Set in the Lambda Management Console, Code, Environment variables section


## [IFTTT](https://ifttt.com/) (IF This Then That) applet setup

The steps to setup this trigger are very simple:
- sign up / login to IFTTT
- create a new applet
- for This, choose _Date & Time every day at 9AM_
- for That, choose Webhooks, with a GET request to the API Gateway URL
- I like to add a query param, like `?ifttt=1` to record the source of the request
