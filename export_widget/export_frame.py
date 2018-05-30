#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (QLabel, QFrame, QGroupBox, QTableView, QComboBox, QPushButton, QFileDialog, QMessageBox,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from custom import PreviewModel


class ExportFrame(QFrame):
    conn: sqlite3.connect = None
    path: str = './'
    model: PreviewModel = None
    writer: pd.ExcelWriter = None
    file_path: str = None

    def __init__(self, *args):
        super(ExportFrame, self).__init__(*args)
        table_group = QGroupBox('Select Table')
        self.table_combo = QComboBox()
        self.table_combo.setFixedWidth(750)
        table_button = QPushButton('&Refresh')
        table_button.setFixedWidth(100)
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table_combo, alignment=Qt.AlignCenter)
        table_layout.addWidget(table_button, alignment=Qt.AlignCenter)
        table_group.setLayout(table_layout)
        table_group.setFixedWidth(884)

        preview_group = QGroupBox('Table Data')
        self.preview_view = QTableView()
        self.preview_view.setFixedSize(860, 516)
        self.format_combo = QComboBox()
        self.format_combo.addItems(['YYYY/MM/DD', 'MM/DD/YYYY', 'DD/MM/YYYY'])
        self.format_combo.setEditable(True)
        self.format_combo.setFixedWidth(100)
        file_button = QPushButton('&File')
        file_button.setFixedWidth(100)
        self.export_button = QPushButton('&Export')
        self.export_button.setFixedWidth(100)
        self.export_button.setEnabled(False)
        self.save_button = QPushButton('&Save')
        self.save_button.setFixedWidth(100)
        self.save_button.setEnabled(False)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(QLabel('Date Format'), alignment=Qt.AlignRight)
        button_layout.addWidget(self.format_combo, alignment=Qt.AlignRight)
        button_layout.addWidget(file_button, alignment=Qt.AlignRight)
        button_layout.addWidget(self.export_button, alignment=Qt.AlignRight)
        button_layout.addWidget(self.save_button, alignment=Qt.AlignRight)
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_view, alignment=Qt.AlignCenter)
        preview_layout.addLayout(button_layout)
        preview_group.setLayout(preview_layout)
        preview_group.setFixedWidth(884)

        main_layout = QVBoxLayout()
        main_layout.addWidget(table_group, alignment=Qt.AlignCenter)
        main_layout.addWidget(preview_group, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

        table_button.clicked.connect(self.get_table)
        self.table_combo.currentTextChanged.connect(self.get_data)
        file_button.clicked.connect(self.export_file)
        self.export_button.clicked.connect(self.export_table)

    def get_table(self):
        c = self.conn.cursor()
        tables = [t[1] for t in c.execute('SELECT * FROM sqlite_master;').fetchall()
                  if t[0] in ('table', 'view') and t[1] not in ('sqlite_sequence')]
        self.table_combo.disconnect()
        self.table_combo.clear()
        self.table_combo.addItems(tables)
        self.table_combo.currentTextChanged.connect(self.get_data)
        self.get_data()
        c.close()

    def get_data(self):
        if self.table_combo.currentText():
            c = self.conn.cursor()
            try:
                data = c.execute(f'SELECT * FROM {self.table_combo.currentText()};').fetchall()
                header = [_[1] for _ in c.execute(f'PRAGMA table_info({self.table_combo.currentText()});').fetchall()]
                dtype = [_[2].upper()
                         for _ in c.execute(f'PRAGMA table_info({self.table_combo.currentText()});').fetchall()]
                if len(data):
                    self.model = PreviewModel(data, header, dtype)
                    self.preview_view.setModel(self.model)
                else:
                    QMessageBox().information(self, 'Error', 'No Result', QMessageBox.Close)
            except sqlite3.OperationalError as error:
                QMessageBox().warning(self, 'Error', f'{error}', QMessageBox.Close)
            c.close()

    def export_file(self):
        file_path: str = QFileDialog.getSaveFileName(self.parent(), 'Export File', self.path, 'Excel File(*.xlsx)',
                                                     options=QFileDialog.DontConfirmOverwrite)[0]
        if file_path:
            self.writer = pd.ExcelWriter(file_path)
            self.file_path = file_path
            self.path = '/'.join(file_path.split('/')[:-1])
            self.export_button.setEnabled(True)

    def export_table(self):
        if self.writer and self.table_combo.currentText():
            c = self.conn.cursor()
            parse_date = [_[1] for _ in c.execute(f'PRAGMA table_info({self.table_combo.currentText()});').fetchall()
                          if _[2] in ('TIMESTAMP', 'NUM')]
            df = pd.read_sql(f'SELECT * FROM {self.table_combo.currentText()};', self.conn, parse_dates=parse_date)
            c.close()
            if 'index' in df.columns.tolist():
                df.drop(columns=['index'], inplace=True)
            df.to_excel(self.writer, self.table_combo.currentText(), index=False)
            self.save_button.setEnabled(True)

    def save_file(self):
        if self.writer:
            wb = load_workbook(self.file_path)
            for ws in wb.worksheets:
                self.format_sheet(ws)
                wb.save(self.file_path)
                wb.close()
                os.startfile(self.file_path)

    def format_sheet(self, worksheet):
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column
            for row_id, cell in enumerate(col):
                if row_id is 0:
                    cell.border = None
                    cell.font = Font(name='Arial', size=10, bold=True)
                    cell.alignment = Alignment('center', 'center')
                    length = max([len(t) for t in str(cell.value).split('\n')])
                else:
                    cell.font = Font(name='Arial', size=10)
                    length = max([len(t) for t in str(cell.value).split('\n')])
                    if cell.is_date:
                        cell.number_format = self.format_combo.currentText()
                        length = 10
                    elif isinstance(cell.value, int):
                        cell.number_format = '0'
                        length = len(str(cell.value))
                if length > max_length:
                    max_length = length
            adjusted_width = max_length
            worksheet.column_dimensions[column].width = max([8, adjusted_width])
