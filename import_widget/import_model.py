#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from openpyxl.utils import get_column_letter


class ImportModel(QAbstractTableModel):
    def __init__(self, titles, *args):
        super(ImportModel, self).__init__(*args)
        self._data = [[title, 'Auto'] for title in titles]
        self._use = [True for _ in titles]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ['Column Name', 'Type Name'][section]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return get_column_letter(section + 1)
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.EditRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.CheckStateRole and index.column() is 0:
            return Qt.Checked if self._use[index.row()] else Qt.Unchecked
        return QVariant()

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        elif index.isValid() and role == Qt.CheckStateRole:
            self._use[index.row()] = True if value == Qt.Checked else False
            return True
        return False

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return QVariant()
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable

    @property
    def dtype(self):
        dtype = {}
        for column_name, type_name in self._data:
            if type_name == 'Text':
                dtype[column_name] = str
            elif type_name == 'Integer':
                dtype[column_name] = np.int64
            elif type_name == 'Percentage':
                dtype[column_name] = np.float64
        return dtype

    @property
    def parse_dates(self):
        return [column_name for column_name, type_name in self._data if type_name == 'Date']

    @property
    def usecols(self):
        return [idx for idx, _ in enumerate(self._use) if _]

    @property
    def table_settings(self):
        return [self._data, self._use]

    @table_settings.setter
    def table_settings(self, table_settings):
        self._data, self._use = table_settings
