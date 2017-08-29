from setuptools import setup

setup(
    name='dojo-monthly-emailer',
    version='0.0.1',
    description='The little bird that spurred the cat herd',
    author='Tom Viner',
    author_email='tom@viner.tv',
    packages=['dojo_emailer'],
    include_package_data=True,
    install_requires=[
        'zappa',
        'Flask',
        'boto3',
        'oauth2client',
        'gspread',
        'logzero',
    ],
    extras_require={
        'test': ['tox'],
        'build': ['pynt', 'isort'],
    },
    license='MIT License',
)
