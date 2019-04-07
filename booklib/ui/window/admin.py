# Filename: booklib/ui/window/admin.py

"""
Main UI Window.
"""

# Standard libraries
import typing

# PyQt5
from PyQt5 import QtWidgets

# BookLib
from booklib import config
from booklib.ui.config import LABELS
from booklib.ui.window.account import AccountWindow
from booklib.ui.window.book import BookWindow


class AdminWindow(QtWidgets.QMainWindow):
    """
    Main admin window.
    """

    def __init__(self, cfg: config.MenuConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = cfg
        self.label_root = __class__.__name__

        # Account window
        self.account_btn = None
        self.account_window = None

        # Book window
        self.book_btn = None
        self.book_window = None

        # Search area
        self.search_textbox = None
        self.search_btn = None
        self.search_output_table = None

        self.init_ui()

    def init_ui(self):
        menu = self.menuBar()
        tools_menu = menu.addMenu('&Tools')

        lang_menu = QtWidgets.QMenu('Language', self)
        lang_en_action = QtWidgets.QAction('English', self)
        lang_en_action.triggered.connect(self.set_lang_en)
        lang_fr_action = QtWidgets.QAction('français', self)
        lang_fr_action.triggered.connect(self.set_lang_fr)
        lang_menu.addAction(lang_en_action)
        lang_menu.addAction(lang_fr_action)

        tools_menu.addMenu(lang_menu)
        self.init_window_ui()

    def init_window_ui(self):
        labels = LABELS[self.cfg.language][self.label_root]

        grid = QtWidgets.QGridLayout()
        vbox_side_menu = QtWidgets.QVBoxLayout()
        # Add account button
        self.account_btn = QtWidgets.QPushButton(labels['account_btn'], self)
        self.account_btn.clicked.connect(self.show_account_window)
        # grid.addWidget(account_btn, 1, 0)
        vbox_side_menu.addWidget(self.account_btn)

        # Add book button
        self.book_btn = QtWidgets.QPushButton(labels['book_btn'], self)
        self.book_btn.clicked.connect(self.show_book_window)
        # grid.addWidget(book_btn, 2, 0)
        vbox_side_menu.addWidget(self.book_btn)

        # Add stretch
        vbox_side_menu.addStretch(1)

        # Add search menu: text bar + button + table
        # TODO - check QCompleter
        hbox_search_menu = QtWidgets.QHBoxLayout()
        self.search_textbox = QtWidgets.QLineEdit()
        hbox_search_menu.addWidget(self.search_textbox)

        self.search_btn = QtWidgets.QPushButton(labels['search_btn'], self)
        self.search_btn.clicked.connect(self.search_entry)
        hbox_search_menu.addWidget(self.search_btn)

        self.search_output_table = QtWidgets.QTableWidget()
        self.search_output_table.setRowCount(10)
        self.search_output_table.setColumnCount(2)
        self.search_output_table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.search_output_table.horizontalHeader().hide()
        self.search_output_table.verticalHeader().hide()
        self.search_output_table.setShowGrid(False)

        vbox_info_menu = QtWidgets.QVBoxLayout()
        vbox_info_menu.addLayout(hbox_search_menu)
        vbox_info_menu.addWidget(self.search_output_table)

        grid.addLayout(vbox_side_menu, 1, 0)
        grid.addLayout(vbox_info_menu, 1, 1)

        # Central widget
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # Set window title
        self.setWindowTitle(labels['title'])

        # Set geometry
        self.setGeometry(0, 0, 300, 100)

        # Move window to center
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Show
        self.show()

    def set_lang_en(self):
        self.cfg.language = 'en'
        self.hide()
        self.init_window_ui()

    def set_lang_fr(self):
        self.cfg.language = 'fr'
        self.hide()
        self.init_window_ui()

    def show_account_window(self):
        if not self.account_window:
            self.account_window = AccountWindow(self)
        self.hide()
        self.account_window.show()

    def show_book_window(self):
        if not self.book_window:
            self.book_window = BookWindow(self)
        self.hide()
        self.book_window.show()

    def search_entry(self):
        pass
