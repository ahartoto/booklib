# Filename: booklib/ui/window/account.py

"""
UI Window for managing accounts.
"""

# PyQt5
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS


class AccountWindow(qtw.QDialog):
    def __init__(self, admin_window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.init_ui()

    def init_ui(self) -> None:
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

        # Create form.
        form_layout = qtw.QFormLayout()
        form_layout.addRow(first_name, first_name_edit)
        form_layout.addRow(family_name, family_name_edit)
        form_layout.addRow(dob, dob_edit)
        form_layout.addRow(gov_id, gov_id_edit)
        form_layout.addRow(phone_no, phone_no_edit)
        form_layout.addRow(school, school_edit)
        form_layout.addRow(level, level_edit)

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
