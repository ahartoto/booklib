# Filename: database.py

"""
Database module provides interfaces and functions to interact with the local
database.
"""

# Standard libraries
import typing

# SQLAlchemy
import sqlalchemy
from sqlalchemy import orm

# BookLib
from booklib import config
from booklib import models


class Session:
    _engine = None

    def __init__(self) -> None:
        if not Session._engine:
            Session._engine = sqlalchemy.create_engine(
                config.get_sqlalchemy_db_path())

        self.engine = Session._engine
        self.__session = orm.sessionmaker(bind=self.engine)()

    def __enter__(self) -> orm.Session:
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb) -> typing.Any:
        if exc_type:
            self.__session.rollback()
            self.__session.close()
            return False

        try:
            self.__session.commit()
            return True
        except Exception:  # pylint: disable=broad-except
            self.__session.rollback()
            return False
        finally:
            self.__session.close()

    @property
    def value(self) -> orm.Session:
        return self.__session


def init(db_session: Session) -> None:
    """Initializes the database."""
    # Create tables
    models.Base.metadata.create_all(db_session.engine)

    # Insert book categories
    with db_session as session:
        for member in models.BookCategoryEnum:
            category = models.BookCategory(category=member.name)
            session.add(category)
