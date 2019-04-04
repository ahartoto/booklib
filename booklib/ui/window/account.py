# Filename: booklib/ui/window/account.py

"""
UI Window for managing accounts.
"""

# PyQt5
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS


class AccountInfo:
    """Stores information of an account.

    The information is stored in the Qt widget.
    """

    def __init__(self):
        self.first_name_qt = qtw.QLineEdit()
        self.first_name_qt.setPlaceholderText('e.g. John')

        self.family_name_qt = qtw.QLineEdit()
        self.family_name_qt.setPlaceholderText('e.g. Doe')

        self.dob_qt = qtw.QDateEdit()
        self.dob_qt.setDisplayFormat('yyyy-MM-dd')
        self.dob_qt.setDate(qtc.QDate.currentDate())
        self.dob_qt.setMaximumDate(qtc.QDate.currentDate())
        self.dob_qt.setCalendarPopup(True)

        self.gov_id_qt = qtw.QLineEdit()

        self.phone_no_qt = qtw.QLineEdit()

        self.school_qt = qtw.QLineEdit()

        self.level_qt = qtw.QLineEdit()


class AccountWindow(qtw.QDialog):
    def __init__(self, admin_window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.account = AccountInfo()

        self.init_ui()

    def init_ui(self) -> None:
        lang = self.admin_window.cfg.language
        labels = LABELS[lang][self.label_root]

        first_name = qtw.QLabel(labels['first_name_txt'])
        family_name = qtw.QLabel(labels['family_name_txt'])
        dob = qtw.QLabel(labels['dob_txt'])
        gov_id = qtw.QLabel(labels['gov_id_txt'])
        phone_no = qtw.QLabel(labels['phone_number_txt'])
        school = qtw.QLabel(labels['school_txt'])
        level = qtw.QLabel(labels['class_level_txt'])

        # Create form.
        form_layout = qtw.QFormLayout()
        form_layout.addRow(first_name, self.account.first_name_qt)
        form_layout.addRow(family_name, self.account.family_name_qt)
        form_layout.addRow(dob, self.account.dob_qt)
        form_layout.addRow(gov_id, self.account.gov_id_qt)
        form_layout.addRow(phone_no, self.account.phone_no_qt)
        form_layout.addRow(school, self.account.school_qt)
        form_layout.addRow(level, self.account.level_qt)

        # Add confirmation buttons at the bottom.
        button_box = qtw.QDialogButtonBox()
        button_box.addButton(labels['ok_btn'], qtw.QDialogButtonBox.AcceptRole)
        button_box.addButton(labels['cancel_btn'],
                             qtw.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.insert_account)
        button_box.rejected.connect(self.show_admin_window)

        form_group_box = qtw.QGroupBox(labels['new_account_form'])
        form_group_box.setLayout(form_layout)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

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

    def show_admin_window(self) -> None:
        self.hide()
        self.admin_window.show()

    def insert_account(self):
        pass
