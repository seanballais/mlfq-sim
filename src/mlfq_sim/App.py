#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets

from mlfq_sim import __version__
from mlfq_sim.gui import main_window

__author__ = "Sean Francis N. Ballais, Warren Kenn H. Pulma"
__copyright__ = "Sean Francis N. Ballais, Warren Kenn H. Pulma"
__license__ = "mit"

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = main_window.Ui_AppWindow()
        self.ui.setupUi(self)


def run():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
