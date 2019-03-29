# Filename: database.py

"""
Database module provides interfaces and functions to interact with the local
database.
"""

# Standard libraries
from contextlib import contextmanager

# SQLAlchemy
from sqlalchemy.orm import sessionmaker

# BookLib
from booklib import models

# Session maker based on the given database engine.
_session = sessionmaker(bind=models.ENGINE)


@contextmanager
def session():
    """Creates a database session."""
    db_session = _session()
    try:
        yield db_session
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def init():
    """Initializes the database."""
    # Create tables
    models.Base.metadata.create_all(models.ENGINE)

    # Insert book categories
    with session() as db_session:
        for member in models.BookCategoryEnum:
            category = models.BookCategory(category=member.name)
            db_session.add(category)
