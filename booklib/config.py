# Filename: booklib/config.py

"""
Config module provides the relevant configurations that are retained within
and across sessions.
"""

# Standard libraries
import datetime
import typing

# Constants
AGE_REQUIRE_ID = 16

# FIXME - change this path
DB_PATH = 'test.db'
SQLALCHEMY_DB_PATH = 'sqlite:///{}'.format(DB_PATH)

# Create a new type
DateTimeType = typing.NewType('DateTime', datetime.datetime)


class MenuConfig:
    """Menu configurations for the UI."""
    def __init__(self, lang: typing.Text = 'en') -> None:
        self._lang = lang

    @property
    def language(self) -> typing.Text:
        return self._lang

    @language.setter
    def language(self, lang: typing.Text) -> None:
        self._lang = lang
