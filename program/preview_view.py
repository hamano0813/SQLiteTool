#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent


class PreviewView(QTableView):
    def __init__(self, parent=None):
        super(PreviewView, self).__init__(parent)
        self.setSelectionBehavior(QTableView.SelectRows | QTableView.SelectColumns)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
