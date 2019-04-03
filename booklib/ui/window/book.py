# Filename: booklib/ui/window/book.py

"""
UI Window for managing books.
"""

# PyQt5
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS


class BookWindow(qtw.QDialog):
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

        # Create forms.
        form_layout = qtw.QFormLayout()
        form_layout.addRow(isbn_no, isbn_no_edit)
        form_layout.addRow(call_no, call_no_edit)

        # Add confirmation buttons at the bottom.
        button_box = qtw.QDialogButtonBox()
        button_box.addButton(labels['ok_btn'], qtw.QDialogButtonBox.AcceptRole)
        button_box.addButton(labels['cancel_btn'],
                             qtw.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.insert_book)
        button_box.rejected.connect(self.show_admin_window)

        form_group_box = qtw.QGroupBox()
        form_group_box.setLayout(form_layout)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

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
