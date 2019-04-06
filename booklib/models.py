# Filename: model.py

"""
Database models of BookLib application.
"""

# Standard libraries
import datetime
import enum

from dateutil.relativedelta import relativedelta

# SQLAlchemy
from sqlalchemy import (
    Column, Date, DateTime,
    Enum, ForeignKey, Integer,
    String, Table,
    create_engine,
)
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship

# BookLib
from booklib import config


# Constants / globals
ENGINE = create_engine(config.SQLALCHEMY_DB_PATH)

Base = declarative_base()


class IdMixin:
    """Mixin to add id column to the database table."""
    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)


class DateMixin:
    """Mixin to add date created and updated columns to database table."""
    @declared_attr
    def date_created(self):
        return Column(DateTime, nullable=False,
                      default=datetime.datetime.utcnow())

    @declared_attr
    def date_updated(self):
        return Column(DateTime, nullable=False,
                      default=datetime.datetime.utcnow())


class ItemMixin:
    """Mixin to add columns associated with a library item."""
    @declared_attr
    def item_id(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def catalog_time(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def borrow_time(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def return_time(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def due_time(self):
        return Column(DateTime, nullable=False)

    # FIXME - add note column?


# Table relationship between two tables: books and authors.
book_author_assoc_table = Table(
    'book_author_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id')),
)


class BookCategoryEnum(enum.Enum):
    children = 1
    adult = 2
    young_adult = 3
    teen = 4
    animals = 5
    nature = 6
    religious = 7
    comic = 8
    others = 9


class ReadingLevelEnum(enum.Enum):
    early_reader = 1
    one_to_three = 2
    four_to_six = 3
    middle_school = 4
    high_school = 5
    advanced = 6
    others = 7


class Book(IdMixin, DateMixin, ItemMixin, Base):
    __tablename__ = 'books'

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='books')

    isbn_number = Column(Integer, nullable=False, index=True)
    call_number = Column(Integer, nullable=False, index=True)
    categories = relationship('BookCategory', back_populates='book')
    level = Column(Enum(ReadingLevelEnum), nullable=False)
    title = Column(String(256), nullable=False, index=True)
    authors = relationship('Author', secondary=book_author_assoc_table,
                           back_populates='books')
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship('Publisher', back_populates='books')


class BookCategory(IdMixin, Base):
    __tablename__ = 'book_categories'

    category = Column(String(20), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='categories')


class Author(IdMixin, Base):
    __tablename__ = 'authors'

    name = Column(String(256), index=True)
    books = relationship('Book', secondary=book_author_assoc_table,
                         back_populates='authors')


class Publisher(IdMixin, Base):
    __tablename__ = 'publishers'

    name = Column(String(256), index=True)
    books = relationship('Book', back_populates='publisher')


class User(IdMixin, DateMixin, Base):
    __tablename__ = 'users'

    family_name = Column(String(256), nullable=False, index=True)
    first_name = Column(String(256), index=True)
    dob = Column(Date, nullable=False)
    gov_id = Column(String(256))
    phone_number = Column(String(20), nullable=False)
    school_name = Column(String(256))
    # FIXME - which enum?
    class_level = Column(Enum)
    books = relationship('Book', back_populates='user')

    # FIXME - add these columns
    # guardian_id = Column(Integer)
    # flag (if book was lost/destroyed)
    # flag date
    # note

    def __repr__(self):
        return '<User "{}, {}">'.format(self.family_name, self.first_name)

    @property
    def require_gov_id(self):
        diff = relativedelta(years=config.AGE_REQUIRE_ID)
        years_ago = datetime.datetime.utcnow() - diff
        return self.dob > years_ago

    @property
    def require_guardian(self):
        return not self.require_gov_id
