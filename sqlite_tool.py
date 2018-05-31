#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QStyleFactory
import sys
from program.main_window import MainWindow

__author__ = 'Hamano'
__version__ = '1.0'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""*{font: 10pt "Arial";}""")
    # noinspection PyCallByClass,PyArgumentList
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
