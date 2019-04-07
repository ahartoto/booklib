# Filename: tests/ui/window/test_admin.py

# PyQt5
from PyQt5 import QtCore

# BookLib
from booklib import config
from booklib.ui.window import admin


def test_click_account(qtbot):
    cfg = config.MenuConfig()
    window = admin.AdminWindow(cfg)
    qtbot.addWidget(window)

    qtbot.mouseClick(window.account_btn, QtCore.Qt.LeftButton)
    assert window.account_window.isVisible()
    assert not window.isVisible()


def test_click_book(qtbot):
    cfg = config.MenuConfig()
    window = admin.AdminWindow(cfg)
    qtbot.addWidget(window)

    qtbot.mouseClick(window.book_btn, QtCore.Qt.LeftButton)
    assert window.book_window.isVisible()
    assert not window.isVisible()


def test_enter_search_keyword(qtbot):
    cfg = config.MenuConfig()
    window = admin.AdminWindow(cfg)
    qtbot.addWidget(window)

    want = 'test'
    qtbot.keyClicks(window.search_textbox, want)
    assert str(window.search_textbox.text()) == want
