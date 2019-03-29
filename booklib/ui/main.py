

import typing

from PyQt5.QtWidgets import QApplication


def create_app(argv: typing.Iterable[typing.Text]) -> QApplication:
    app = QApplication(argv)
    app.setStyle('Fusion')
    return app
