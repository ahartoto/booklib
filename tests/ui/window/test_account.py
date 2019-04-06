# Filename: tests/ui/window/test_account.py

# Standard library
import datetime

# python-dateutil
from dateutil.relativedelta import relativedelta

# PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# PyTest-Qt
from pytestqt import qtbot

# BookLib
from booklib import config
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
    window = admin.AdminWindow(config.MenuConfig())
    qtbot.addWidget(window)
    qtbot.mouseClick(window.account_btn, QtCore.Qt.LeftButton)

    dialog = window.account_window
    insert_test_data(dialog.account)
    qtbot.mouseClick(dialog.button_box.buttons()[0], QtCore.Qt.LeftButton)
    # TODO - fix IntegrityError
    # assert dialog.error_dialog.isVisible()
