# Filename: booklib/ui/window/book.py

"""
UI Window for cataloging book.
"""

# PyQt5
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS


class AddBookWindow(qtw.QMainWindow):
    def __init__(self, admin_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.init_ui()

    def init_ui(self):
        lang = self.admin_window.cfg.language
        labels = LABELS[lang][self.label_root]

        isbn_no = qtw.QLabel(labels['isbn_no_txt'])
        call_no = qtw.QLabel(labels['call_no_txt'])

        isbn_no_edit = qtw.QLineEdit()
        call_no_edit = qtw.QLineEdit()

        grid = qtw.QGridLayout()

        # Ensure labels are aligned
        grid.setSpacing(10)

        i = 1
        grid.addWidget(isbn_no, i, 0)
        grid.addWidget(isbn_no_edit, i, 1)
        i += 1

        grid.addWidget(call_no, i, 0)
        grid.addWidget(call_no_edit, i, 1)
        i += 1

        # Add buttons at the bottom
        ok_btn = qtw.QPushButton(labels['ok_btn'])
        ok_btn.clicked.connect(self.insert_book)

        cancel_btn = qtw.QPushButton(labels['cancel_btn'])
        cancel_btn.clicked.connect(self.show_admin_window)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        confirm_widget = qtw.QWidget()
        confirm_widget.setLayout(hbox)
        grid.addWidget(confirm_widget, i, 1)
        i += 1

        # Central widget
        central_widget = qtw.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # Set window title
        self.setWindowTitle(labels['title'])

        # Move window to center
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()

    def show_admin_window(self):
        self.hide()
        self.admin_window.show()

    def insert_book(self):
        pass
