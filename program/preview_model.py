#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant


class PreviewModel(QAbstractTableModel):
    def __init__(self, data, header, dtype, *args):
        super(PreviewModel, self).__init__(*args)
        start = 0
        if 'index' in header:
            start = 1
        self._data = [row[start:] for row in data]
        self._header = header[start:]
        self._dtype = dtype[start:]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[section]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section + 1
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._data[0])

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole:
            if self._dtype[index.column()] in ('TIMESTAMP', 'NUM', 'DATE', 'DATETIME'):
                if self._data[index.row()][index.column()]:
                    return pd.to_datetime(self._data[index.row()][index.column()]).strftime('%Y/%m/%d')
                else:
                    return ''
            elif self._data[index.row()][index.column()]:
                return self._data[index.row()][index.column()]
            return ''
        return QVariant()

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return QVariant()
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def copy_range(self, select_range):
        if select_range:
            r = max([index.row() for index in select_range]) - min([index.row() for index in select_range]) + 1
            c = max([index.column() for index in select_range]) - min([index.column() for index in select_range]) + 1
            return '\n'.join(['\t'.join([self.data(select_range[r * rid + c * cid], Qt.DisplayRole)
                                         for cid in range(c)])
                              for rid in range(r)])
