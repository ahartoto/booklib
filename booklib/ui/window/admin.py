# Filename: booklib/ui/window/admin.py

"""
Main UI Window.
"""

# Standard libraries

# PyQt5
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS
from booklib.ui.window.account import AddAccountWindow
from booklib.ui.window.book import AddBookWindow


class AdminWindow(qtw.QMainWindow):
    """
    Main admin window.
    """

    def __init__(self, cfg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = cfg
        self.label_root = __class__.__name__

        # Add Account window
        self.add_account_window = None

        # Add Book window
        self.add_book_window = None

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
        # Add account button
        add_account_btn = qtw.QPushButton(labels['add_account_btn'], self)
        add_account_btn.clicked.connect(self.show_add_account_window)
        grid.addWidget(add_account_btn, 1, 0)

        # Add book button
        add_book_btn = qtw.QPushButton(labels['add_book_btn'], self)
        add_book_btn.clicked.connect(self.show_add_book_window)
        grid.addWidget(add_book_btn, 1, 1)

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

    def show_add_account_window(self):
        if not self.add_account_window:
            self.add_account_window = AddAccountWindow(self)
        self.hide()
        self.add_account_window.show()

    def show_add_book_window(self):
        if not self.add_book_window:
            self.add_book_window = AddBookWindow(self)
        self.hide()
        self.add_book_window.show()
