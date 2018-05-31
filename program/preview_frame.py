#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5.QtWidgets import QLabel, QFrame, QGroupBox, QTableView, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from program.preview_model import PreviewModel
from program.sqlite_highlighter import SQLiteHighlighter
from program.sqlite_completer import SQLiteCompleterText


class PreviewFrame(QFrame):
    conn: sqlite3.connect = None
    model: PreviewModel = None

    def __init__(self, *args):
        super(PreviewFrame, self).__init__(*args)
        select_group = QGroupBox('Select SQL')
        self.select_text = SQLiteCompleterText()
        self.select_text.setFixedSize(750, 130)
        self.highlighter = SQLiteHighlighter(self.select_text.document())
        select_button = QPushButton('&View')
        select_button.setFixedWidth(100)
        select_layout = QHBoxLayout()
        select_layout.addWidget(self.select_text, alignment=Qt.AlignCenter)
        select_layout.addWidget(select_button, alignment=Qt.AlignCenter | Qt.AlignTop)
        select_group.setLayout(select_layout)
        select_group.setFixedWidth(884)

        preview_group = QGroupBox('Preview Select')
        self.preview_view = QTableView()
        self.preview_view.setFixedSize(860, 416)
        self.row_label = QLabel()
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_view, alignment=Qt.AlignCenter)
        preview_layout.addWidget(self.row_label, alignment=Qt.AlignLeft)
        preview_group.setLayout(preview_layout)
        preview_group.setFixedWidth(884)

        main_layout = QVBoxLayout()
        main_layout.addWidget(select_group, alignment=Qt.AlignCenter)
        main_layout.addWidget(preview_group, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

        select_button.clicked.connect(self.preview_sql)

    def preview_sql(self):
        if self.select_text.toPlainText().lstrip()[0:6].upper().startswith('SELECT'):
            c = self.conn.cursor()
            c.execute('DROP VIEW IF EXISTS temp;')
            try:
                c.execute(f'CREATE VIEW temp AS {self.select_text.toPlainText()}')
                data = c.execute(f'SELECT * FROM temp;').fetchall()
                header = [_[1] for _ in c.execute(f'PRAGMA table_info(temp);').fetchall()]
                dtype = [_[2].upper() for _ in c.execute(f'PRAGMA table_info(temp);').fetchall()]
                if len(data):
                    self.model = PreviewModel(data, header, dtype)
                    self.preview_view.setModel(self.model)
                    self.row_label.setText(f'{len(data)} result')
                else:
                    QMessageBox().information(self, 'Error', 'No Result', QMessageBox.Close)
            except sqlite3.OperationalError as error:
                QMessageBox().warning(self, 'Error', f'{error}', QMessageBox.Close)
            c.execute('DROP VIEW IF EXISTS temp;')
            c.close()