# Filename: main.py

import os
import sys
import typing

import booklib.ui.window.admin
from booklib import config
from booklib import database
from booklib import ui


def main(argv: typing.Iterable[typing.Text] = None) -> None:
    if not argv:
        argv = sys.argv[1:]

    # Create database if it doesn't exist yet
    if not os.path.exists(config.get_db_path()):
        session = database.Session()
        database.init(session)

    # Get config
    cfg = config.MenuConfig()

    # Start the main window
    app = ui.main.create_app(argv)
    _ = booklib.ui.window.admin.AdminWindow(cfg)
    app.exec_()
