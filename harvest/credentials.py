import os
from getpass import getpass, getuser
from os import environ


def get_username():
    return os.environ.get('HARVEST_USERNAME') or getuser()


def get_password():
    return os.environ.get('HARVEST_PASSWORD')
