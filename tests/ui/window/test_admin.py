# Filename: tests/ui/window/test_admin.py

# Standard library
import os

# PyQt5
from PyQt5 import QtCore as qtc

# PyTest-Qt
from pytestqt import qtbot

# BookLib
from booklib import config
from booklib.ui.window import admin


def test_click_account(qtbot):
    cfg = config.MenuConfig()
    window = admin.AdminWindow(cfg)
    qtbot.addWidget(window)

    qtbot.mouseClick(window.account_btn, qtc.Qt.LeftButton)
    assert window.account_window.isVisible()
    assert not window.isVisible()


def test_click_book(qtbot):
    cfg = config.MenuConfig()
    window = admin.AdminWindow(cfg)
    qtbot.addWidget(window)

    qtbot.mouseClick(window.book_btn, qtc.Qt.LeftButton)
    assert window.book_window.isVisible()
    assert not window.isVisible()
