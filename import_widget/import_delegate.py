#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate
from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel


class TypeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TypeDelegate, self).__init__(parent)

    def createEditor(self, parent, option, model_index: QModelIndex):
        editor = QComboBox(parent)
        editor.addItems(['Auto', 'Text', 'Integer', 'Date', 'Percentage'])
        return editor

    def setEditorData(self, editor: QComboBox, model_index: QModelIndex):
        data = model_index.model().data(model_index, Qt.DisplayRole)
        editor.setCurrentText(data)

    def setModelData(self, editor: QComboBox, item_model: QAbstractItemModel, model_index: QModelIndex):
        item_model.setData(model_index, editor.currentText())

    def updateEditorGeometry(self, editor: QComboBox, option, model_index: QModelIndex):
        editor.setGeometry(option.rect)
