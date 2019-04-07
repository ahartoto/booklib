# Filename: booklib/config.py

"""
Config module provides the relevant configurations that are retained within
and across sessions.
"""

# Standard libraries
import datetime
import os
import typing

# Constants
AGE_REQUIRE_ID = 16

# Create a new type
DateTimeType = typing.NewType('DateTime', datetime.datetime)


def get_db_path() -> typing.Text:
    """Retrieve the database path.

    User can set the path as an environment variable ($BOOKLIB_DB_PATH).

    Returns:
        Path to where the database is.
    """
    return os.getenv('BOOKLIB_DB_PATH', 'booklib.db')


def get_sqlalchemy_db_path() -> typing.Text:
    """Retrieve the database path that is compatible with SQLAlchemy.

    Returns:
        Path used by SQLAlchemy to create the engine.
    """
    return 'sqlite:///{}'.format(get_db_path())


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
