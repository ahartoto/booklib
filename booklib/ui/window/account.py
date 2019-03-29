# Filename: booklib/ui/window/account.py

"""
UI Window for adding a new account.
"""

# PyQt5
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS


class AddAccountWindow(qtw.QMainWindow):
    def __init__(self, admin_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.init_ui()

    def init_ui(self):
        lang = self.admin_window.cfg.language
        labels = LABELS[lang][self.label_root]

        first_name = qtw.QLabel(labels['first_name_txt'])
        first_name_edit = qtw.QLineEdit()

        family_name = qtw.QLabel(labels['family_name_txt'])
        family_name_edit = qtw.QLineEdit()

        dob = qtw.QLabel(labels['dob_txt'])
        dob_edit = qtw.QDateEdit()
        dob_edit.setDisplayFormat('yyyy-MM-dd')
        dob_edit.setDate(qtc.QDate.currentDate())
        dob_edit.setMaximumDate(qtc.QDate.currentDate())
        dob_edit.setCalendarPopup(True)

        gov_id = qtw.QLabel(labels['gov_id_txt'])
        gov_id_edit = qtw.QLineEdit()

        phone_no = qtw.QLabel(labels['phone_number_txt'])
        phone_no_edit = qtw.QLineEdit()

        school = qtw.QLabel(labels['school_txt'])
        school_edit = qtw.QLineEdit()

        level = qtw.QLabel(labels['class_level_txt'])
        level_edit = qtw.QLineEdit()

        grid = qtw.QGridLayout()

        # Ensure labels are aligned
        grid.setSpacing(10)

        i = 1
        grid.addWidget(first_name, i, 0)
        grid.addWidget(first_name_edit, i, 1)
        i += 1

        grid.addWidget(family_name, i, 0)
        grid.addWidget(family_name_edit, i, 1)
        i += 1

        grid.addWidget(dob, i, 0)
        grid.addWidget(dob_edit, i, 1)
        i += 1

        grid.addWidget(gov_id, i, 0)
        grid.addWidget(gov_id_edit, i, 1)
        i += 1

        grid.addWidget(phone_no, i, 0)
        grid.addWidget(phone_no_edit, i, 1)
        i += 1

        grid.addWidget(school, i, 0)
        grid.addWidget(school_edit, i, 1)
        i += 1

        grid.addWidget(level, i, 0)
        grid.addWidget(level_edit, i, 1)
        i += 1

        # Add buttons at the bottom
        ok_btn = qtw.QPushButton(labels['ok_btn'])
        ok_btn.clicked.connect(self.insert_account)

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

        # Set geometry
        # self.setGeometry(0, 0, 300, 200)

        # Lock size
        # self.setFixedSize(self.size())

        # Move window to center
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()

    def show_admin_window(self):
        self.hide()
        self.admin_window.show()

    def insert_account(self):
        pass
