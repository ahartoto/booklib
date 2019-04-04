# Filename: booklib/ui/window/book.py

"""
UI Window for managing books.
"""

# PyQt5
import PyQt5.QtWidgets as qtw

# BookLib
from booklib.ui.config import LABELS

# BookLib
from booklib.models import BookCategoryEnum


class BookInfo:

    def __init__(self):
        self.isbn_no_qt = qtw.QLineEdit()
        self.call_no_qt = qtw.QLineEdit()

        self.categories_children_qt = qtw.QCheckBox(
            BookCategoryEnum.children.name)
        self.categories_adult_qt = qtw.QCheckBox(BookCategoryEnum.adult.name)
        self.categories_young_adult_qt = qtw.QCheckBox(
            BookCategoryEnum.young_adult.name)
        self.categories_teen_qt = qtw.QCheckBox(BookCategoryEnum.teen.name)
        self.categories_animals_qt = qtw.QCheckBox(
            BookCategoryEnum.animals.name)
        self.categories_nature_qt = qtw.QCheckBox(BookCategoryEnum.nature.name)
        self.categories_religious_qt = qtw.QCheckBox(
            BookCategoryEnum.religious.name)
        self.categories_comic_qt = qtw.QCheckBox(BookCategoryEnum.comic.name)
        self.categories_others_qt = qtw.QCheckBox(BookCategoryEnum.others.name)

        self.categories_box_qt = qtw.QGroupBox()
        categories_layout = qtw.QGridLayout()
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


class BookWindow(qtw.QDialog):
    def __init__(self, admin_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_root = __class__.__name__
        self.admin_window = admin_window

        self.book = BookInfo()

        self.init_ui()

    def init_ui(self):
        lang = self.admin_window.cfg.language
        labels = LABELS[lang][self.label_root]

        isbn_no = qtw.QLabel(labels['isbn_no_txt'])
        call_no = qtw.QLabel(labels['call_no_txt'])
        categories = qtw.QLabel(labels['category_txt'])

        # Create forms.
        form_layout = qtw.QFormLayout()
        form_layout.addRow(isbn_no, self.book.isbn_no_qt)
        form_layout.addRow(call_no, self.book.call_no_qt)
        form_layout.addRow(categories, self.book.categories_box_qt)

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
