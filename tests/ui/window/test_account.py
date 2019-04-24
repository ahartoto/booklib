# Filename: tests/ui/window/test_account.py

# Standard library
import datetime
import os

# python-dateutil
from dateutil.relativedelta import relativedelta

# PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# BookLib
from booklib import config
from booklib import database
from booklib.ui.window import account
from booklib.ui.window import admin


def insert_test_data(info: account.AccountInfo) -> None:
    info.first_name_qt.setText('test_first_name')
    info.family_name_qt.setText('test_family_name')
    info.phone_no_qt.setText('test_phone_number')

    today = datetime.date.today()
    fifteen_years_ago = today - relativedelta(years=15)
    info.dob_qt.setDate(fifteen_years_ago)


def test_account_no_first_name(qtbot):
    os.environ['BOOKLIB_DB_PATH'] = ':memory:'
    database.init(database.Session())

    window = admin.AdminWindow(config.MenuConfig())
    qtbot.addWidget(window)
    qtbot.mouseClick(window.account_btn, QtCore.Qt.LeftButton)

    dialog = window.account_window
    insert_test_data(dialog.account)
    dialog.account.first_name_qt.setText('')
    qtbot.mouseClick(dialog.button_box.buttons()[0], QtCore.Qt.LeftButton)
    assert dialog.error_dialog.isVisible()


def test_account_focus_on_first_name(qtbot):
    os.environ['BOOKLIB_DB_PATH'] = ':memory:'
    database.init(database.Session())

    window = admin.AdminWindow(config.MenuConfig())
    qtbot.addWidget(window)
    qtbot.mouseClick(window.account_btn, QtCore.Qt.LeftButton)

    dialog = window.account_window
    assert dialog.isVisible()
    if not os.getenv('TRAVIS'):
        assert dialog.account.first_name_qt.hasFocus()


def test_account_clear_button(qtbot):
    os.environ['BOOKLIB_DB_PATH'] = ':memory:'
    database.init(database.Session())

    window = admin.AdminWindow(config.MenuConfig())
    qtbot.addWidget(window)
    qtbot.mouseClick(window.account_btn, QtCore.Qt.LeftButton)

    dialog = window.account_window

    # Move focus to another line
    dialog.account.family_name_qt.setFocus()
    dialog.account.family_name_qt.setText('random')
    if not os.getenv('TRAVIS'):
        qtbot.waitUntil(lambda: dialog.account.family_name_qt.hasFocus())

    qtbot.mouseClick(dialog.button_box.buttons()[2], QtCore.Qt.LeftButton)
    assert dialog.isVisible()
    assert not str(dialog.account.family_name_qt.text())
    if not os.getenv('TRAVIS'):
        assert dialog.account.first_name_qt.hasFocus()
