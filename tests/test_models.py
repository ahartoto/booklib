# Filename: tests/test_models.py

# Standard libraries
import datetime
import os

# BookLib
from booklib import database
from booklib import models


class TestUser:
    def setup_method(self):
        os.environ['BOOKLIB_DB_PATH'] = ':memory:'
        session = database.Session()
        database.init(session)
        self.connection = session.engine.connect()
        self.tx = self.connection.begin()
        self.session = session.value

    def teardown_method(self):
        self.session.close()
        self.tx.rollback()
        self.connection.close()

    def test_insert_one_user(self):
        user = models.User(
            first_name='ut_first_name',
            family_name='ut_family_name',
            dob=datetime.date.today(),
            phone_number='12345',
        )
        self.session.add(user)
        self.session.commit()
