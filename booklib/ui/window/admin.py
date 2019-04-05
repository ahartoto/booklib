# Filename: booklib/ui/window/admin.py

"""
Main UI Window.
"""

# Standard libraries
import typing

# PyQt5
import PyQt5.QtWidgets as qtw

# BookLib
from booklib import config
from booklib.ui.config import LABELS
from booklib.ui.window.account import AccountWindow
from booklib.ui.window.book import BookWindow


class AdminWindow(qtw.QMainWindow):
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

        self.init_ui()

    def init_ui(self):
        menu = self.menuBar()
        tools_menu = menu.addMenu('&Tools')

        lang_menu = qtw.QMenu('Language', self)
        lang_en_action = qtw.QAction('English', self)
        lang_en_action.triggered.connect(self.set_lang_en)
        lang_fr_action = qtw.QAction('français', self)
        lang_fr_action.triggered.connect(self.set_lang_fr)
        lang_menu.addAction(lang_en_action)
        lang_menu.addAction(lang_fr_action)

        tools_menu.addMenu(lang_menu)
        self.init_window_ui()

    def init_window_ui(self):
        labels = LABELS[self.cfg.language][self.label_root]

        grid = qtw.QGridLayout()
        vbox_side_menu = qtw.QVBoxLayout()
        # Add account button
        self.account_btn = qtw.QPushButton(labels['account_btn'], self)
        self.account_btn.clicked.connect(self.show_account_window)
        # grid.addWidget(account_btn, 1, 0)
        vbox_side_menu.addWidget(self.account_btn)

        # Add book button
        self.book_btn = qtw.QPushButton(labels['book_btn'], self)
        self.book_btn.clicked.connect(self.show_book_window)
        # grid.addWidget(book_btn, 2, 0)
        vbox_side_menu.addWidget(self.book_btn)

        # Add search menu: text bar + button
        hbox_search_menu = qtw.QHBoxLayout()
        search_textbox = qtw.QLineEdit()
        hbox_search_menu.addWidget(search_textbox)

        search_btn = qtw.QPushButton(labels['search_btn'], self)
        search_btn.clicked.connect(self.search_entry)
        hbox_search_menu.addWidget(search_btn)

        vbox_info_menu = qtw.QVBoxLayout()
        vbox_info_menu.addLayout(hbox_search_menu)

        grid.addLayout(vbox_side_menu, 1, 0)
        grid.addLayout(vbox_info_menu, 1, 1)

        # Central widget
        central_widget = qtw.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # Set window title
        self.setWindowTitle(labels['title'])

        # Set geometry
        self.setGeometry(0, 0, 300, 100)

        # Move window to center
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
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
