# Filename: booklib/ui/window/account.py

"""
UI Window for managing accounts.
"""

# Standard libraries
import datetime
import typing

# PyQt5
from PyQt5 import QtCore
from PyQt5 import QtWidgets

# BookLib
from booklib import config
from booklib import database
from booklib import errors
from booklib.ui.config import LABELS


def text_value(widget: QtWidgets.QLineEdit) -> typing.Union[None, typing.Text]:
    if widget.text():
        return str(widget.text())
    return None


class AccountInfo:
    """Stores information of an account.

    The information is stored in the Qt widget.
    """

    def __init__(self, labels: typing.Mapping[typing.Text, typing.Any]):
        self.labels = labels

        self.first_name_qt = QtWidgets.QLineEdit()
        self.first_name_qt.setPlaceholderText('e.g. John')

        self.family_name_qt = QtWidgets.QLineEdit()
        self.family_name_qt.setPlaceholderText('e.g. Doe')

        self.dob_qt = QtWidgets.QDateEdit()
        self.dob_qt.setDisplayFormat('yyyy-MM-dd')
        self.dob_qt.setDate(QtCore.QDate.currentDate())
        self.dob_qt.setMaximumDate(QtCore.QDate.currentDate())
        self.dob_qt.setCalendarPopup(True)

        self.gov_id_qt = QtWidgets.QLineEdit()

        self.phone_no_qt = QtWidgets.QLineEdit()

        self.school_qt = QtWidgets.QLineEdit()

        self.level_qt = QtWidgets.QLineEdit()

    @property
    def data(self) -> database.models.User:
        return database.models.User(
            first_name=str(self.first_name_qt.text()),
            family_name=str(self.family_name_qt.text()),
            dob=self.dob_qt.date().toPyDate(),
            gov_id=text_value(self.gov_id_qt),
            phone_number=str(self.phone_no_qt.text()),
            school_name=text_value(self.school_qt),
        )

    def clear(self) -> None:
        self.first_name_qt.clear()
        self.family_name_qt.clear()
        self.dob_qt.setDate(QtCore.QDate.currentDate())
        self.gov_id_qt.clear()
        self.phone_no_qt.clear()
        self.school_qt.clear()
        self.level_qt.clear()

    def validate(self) -> None:
        # Validate name
        if not self.first_name_qt.text():
            raise errors.InputDataError(self.labels['errors']['no_first_name'])
        if not self.family_name_qt.text():
            raise errors.InputDataError(self.labels['errors']['no_last_name'])

        # Validate phone number
        if not self.phone_no_qt.text():
            msg = self.labels['errors']['no_phone_number']
            raise errors.InputDataError(msg)

        dob = self.dob_qt.date().toPyDate()
        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month,
                                                                   dob.day))
        if age >= config.AGE_REQUIRE_ID:
            if not self.gov_id_qt.text():
                msg = self.labels['errors']['no_gov_id']
                raise errors.InputDataError(msg.format(config.AGE_REQUIRE_ID))
        else:
            # TODO - add check of guardian
            pass


class AccountWindow(QtWidgets.QDialog):
    def __init__(self, admin_window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.account = None
        self.button_box = None
        self.error_dialog = None

        self.init_ui()

    def init_ui(self) -> None:
        lang = self.admin_window.cfg.language
        labels = LABELS[lang][self.label_root]

        self.account = AccountInfo(labels)

        first_name = QtWidgets.QLabel(labels['first_name_txt'])
        family_name = QtWidgets.QLabel(labels['family_name_txt'])
        dob = QtWidgets.QLabel(labels['dob_txt'])
        gov_id = QtWidgets.QLabel(labels['gov_id_txt'])
        phone_no = QtWidgets.QLabel(labels['phone_number_txt'])
        school = QtWidgets.QLabel(labels['school_txt'])
        level = QtWidgets.QLabel(labels['class_level_txt'])

        # Create form.
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(first_name, self.account.first_name_qt)
        form_layout.addRow(family_name, self.account.family_name_qt)
        form_layout.addRow(phone_no, self.account.phone_no_qt)
        form_layout.addRow(dob, self.account.dob_qt)
        form_layout.addRow(gov_id, self.account.gov_id_qt)
        form_layout.addRow(school, self.account.school_qt)
        form_layout.addRow(level, self.account.level_qt)

        # Add confirmation buttons at the bottom.
        self.button_box = QtWidgets.QDialogButtonBox()
        self.button_box.addButton(labels['ok_btn'],
                                  QtWidgets.QDialogButtonBox.AcceptRole)
        clear_btn = self.button_box.addButton(
            labels['clear_btn'], QtWidgets.QDialogButtonBox.ResetRole)
        self.button_box.addButton(labels['cancel_btn'],
                                  QtWidgets.QDialogButtonBox.RejectRole)
        self.button_box.accepted.connect(self.insert_account)
        self.button_box.rejected.connect(self.show_admin_window)
        clear_btn.clicked.connect(self.clear_account_data)

        form_group_box = QtWidgets.QGroupBox(labels['new_account_form'])
        form_group_box.setLayout(form_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

        # Set window title
        self.setWindowTitle(labels['title'])

        # Set geometry
        # self.setGeometry(0, 0, 300, 200)

        # Lock size
        # self.setFixedSize(self.size())

        # Move window to center
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.account.first_name_qt.setFocus()
        self.show()

    def show_admin_window(self) -> None:
        self.hide()
        self.admin_window.show()

    def clear_account_data(self) -> None:
        self.account.clear()
        self.account.first_name_qt.setFocus()

    def insert_account(self) -> None:
        try:
            self.account.validate()
        except errors.InputDataError as e:
            self.error_dialog = QtWidgets.QErrorMessage(self)
            self.error_dialog.setWindowModality(QtCore.Qt.WindowModal)
            self.error_dialog.showMessage(str(e))
            return

        with database.Session() as session:
            session.add(self.account.data)

        self.clear_account_data()
        self.show_admin_window()

