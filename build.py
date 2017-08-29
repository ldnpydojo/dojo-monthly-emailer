import os

from pynt import task

from dojo_emailer.app import app


@task()
def clean():
    '''Remove extraneous files/folders, with manual approval.'''
    os.system('git clean --interactive -d -x')


@task()
def isort():
    '''Sort python import statements.'''
    # skip dot files/folders
    os.system('isort --recursive --apply --skip-glob=".?*"')


@task()
def devserver():
    '''Start server locally, in debug mode.'''
    app.run(debug=True)
