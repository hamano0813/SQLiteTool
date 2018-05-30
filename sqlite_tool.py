#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QStyleFactory
import sys
from program import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""*{font: 9pt "Arial";}""")
    # noinspection PyCallByClass,PyArgumentList
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
