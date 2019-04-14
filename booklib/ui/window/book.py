# Filename: booklib/ui/window/book.py

"""
UI Window for managing books.
"""

# Standard libraries
import typing

# PyQt5
from PyQt5 import QtCore
from PyQt5 import QtWidgets

# BookLib
from booklib import database
from booklib import errors
from booklib import models
from booklib.ui.config import LABELS


class BookInfo:

    def __init__(self, labels: typing.Mapping[typing.Text, typing.Any]):
        self.labels = labels

        self.isbn_no_qt = QtWidgets.QLineEdit()
        self.call_no_qt = QtWidgets.QLineEdit()

        categories = labels['categories_checkboxes']
        name = categories[models.BookCategoryEnum.children.name]
        self.categories_children_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.adult.name]
        self.categories_adult_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.young_adult.name]
        self.categories_young_adult_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.teen.name]
        self.categories_teen_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.animals.name]
        self.categories_animals_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.nature.name]
        self.categories_nature_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.religious.name]
        self.categories_religious_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.comic.name]
        self.categories_comic_qt = QtWidgets.QCheckBox(name)

        name = categories[models.BookCategoryEnum.others.name]
        self.categories_others_qt = QtWidgets.QCheckBox(name)

        self.categories_box_qt = QtWidgets.QGroupBox()
        categories_layout = QtWidgets.QGridLayout()
        categories_layout.addWidget(self.categories_children_qt, 1, 0)
        categories_layout.addWidget(self.categories_adult_qt, 1, 1)
        categories_layout.addWidget(self.categories_young_adult_qt, 2, 0)
        categories_layout.addWidget(self.categories_teen_qt, 2, 1)
        categories_layout.addWidget(self.categories_animals_qt, 3, 0)
        categories_layout.addWidget(self.categories_nature_qt, 3, 1)
        categories_layout.addWidget(self.categories_religious_qt, 4, 0)
        categories_layout.addWidget(self.categories_comic_qt, 4, 1)
        categories_layout.addWidget(self.categories_others_qt, 5, 0)
        self.categories_box_qt.setLayout(categories_layout)

        self.reading_level_qt = QtWidgets.QComboBox()
        # Add empty string as default.
        self.reading_level_qt.addItem('')

        levels = labels['reading_levels']
        for level in models.ReadingLevelEnum:
            self.reading_level_qt.addItem(levels[level.name])
        # self.reading_level_qt.activated[str].connect()

        self.title_qt = QtWidgets.QLineEdit()
        self.author_qt = QtWidgets.QLineEdit()

        self.publisher_qt = QtWidgets.QLineEdit()
        publisher_completer = QtWidgets.QCompleter()
        publisher_model = QtCore.QStringListModel()

        # Find all publishers that have been added.
        with database.Session() as session:
            publishers = session.query(models.Publisher).all()
            publisher_model.setStringList(publishers)
        self.publisher_qt.setCompleter(publisher_completer)

    @property
    def data(self) -> database.models.Book:
        return database.models.Book(
            isbn_number=int(self.isbn_no_qt.text()),
            call_number=int(self.call_no_qt.text()),
        )

    def clear(self) -> None:
        self.isbn_no_qt.setText('')
        self.call_no_qt.setText('')
        self.categories_children_qt.setChecked(False)
        self.categories_adult_qt.setChecked(False)
        self.categories_young_adult_qt.setChecked(False)
        self.categories_teen_qt.setChecked(False)
        self.categories_animals_qt.setChecked(False)
        self.categories_nature_qt.setChecked(False)
        self.categories_religious_qt.setChecked(False)
        self.categories_comic_qt.setChecked(False)
        self.categories_others_qt.setChecked(False)
        self.reading_level_qt.setCurrentIndex(0)
        self.title_qt.setText('')
        self.author_qt.setText('')
        self.publisher_qt.setText('')

    def validate(self) -> None:
        isbn_no_txt = self.isbn_no_qt.text()
        if not isbn_no_txt:
            raise errors.InputDataError(self.labels['errors']['no_isbn'])
        try:
            int(isbn_no_txt)
        except ValueError:
            raise errors.InputDataError(self.labels['errors']['invalid_isbn'])


class BookWindow(QtWidgets.QDialog):
    def __init__(self, admin_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.book = None
        self.error_dialog = None

        self.init_ui()

    def init_ui(self):
        lang = self.admin_window.cfg.language
        labels = LABELS[lang][self.label_root]

        self.book = BookInfo(labels)

        isbn_no = QtWidgets.QLabel(labels['isbn_no_txt'])
        call_no = QtWidgets.QLabel(labels['call_no_txt'])
        title = QtWidgets.QLabel(labels['title_txt'])
        authors = QtWidgets.QLabel(labels['authors_txt'])
        publisher = QtWidgets.QLabel(labels['publisher_txt'])
        categories = QtWidgets.QLabel(labels['category_txt'])
        reading_level = QtWidgets.QLabel(labels['level_txt'])

        # Create forms.
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(isbn_no, self.book.isbn_no_qt)
        form_layout.addRow(call_no, self.book.call_no_qt)
        form_layout.addRow(title, self.book.title_qt)
        form_layout.addRow(authors, self.book.author_qt)
        form_layout.addRow(publisher, self.book.publisher_qt)
        form_layout.addRow(categories, self.book.categories_box_qt)
        form_layout.addRow(reading_level, self.book.reading_level_qt)

        # Add confirmation buttons at the bottom.
        button_box = QtWidgets.QDialogButtonBox()
        button_box.addButton(labels['ok_btn'], QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.addButton(labels['cancel_btn'],
                             QtWidgets.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.insert_book)
        button_box.rejected.connect(self.show_admin_window)

        form_group_box = QtWidgets.QGroupBox()
        form_group_box.setLayout(form_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

        # Set window title
        self.setWindowTitle(labels['title'])

        # Move window to center
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()

    def clear_book_data(self) -> None:
        self.book.clear()

    def show_admin_window(self) -> None:
        self.hide()
        self.admin_window.show()

    def insert_book(self) -> None:
        try:
            self.book.validate()
        except errors.InputDataError as e:
            self.error_dialog = QtWidgets.QErrorMessage(self)
            self.error_dialog.setWindowModality(QtCore.Qt.WindowModal)
            self.error_dialog.showMessage(str(e))
            return

        # FIXME - add entry to session
        # with database.Session() as session:
        #     session.add(self.book.data)

        self.clear_book_data()
        self.show_admin_window()
