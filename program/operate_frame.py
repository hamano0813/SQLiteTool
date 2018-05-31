#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5.QtWidgets import QFrame, QGroupBox, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from program.sqlite_highlighter import SQLiteHighlighter
from program.sqlite_completer import SQLiteCompleterText


class OperateFrame(QFrame):
    conn: sqlite3.connect = None
    path: str = './setting/'

    def __init__(self, *args):
        super(OperateFrame, self).__init__(*args)
        sql_group = QGroupBox('SQL Database Operate', self)
        self.stmt_text = SQLiteCompleterText()
        self.stmt_text.setFixedSize(860, 585)
        self.stmt_text.setStatusTip('split with ";"')
        self.highlighter = SQLiteHighlighter(self.stmt_text.document())
        save_button = QPushButton('&Save')
        save_button.setFixedWidth(100)
        load_button = QPushButton('&Load')
        load_button.setFixedWidth(100)
        execute_button = QPushButton('&Execute')
        execute_button.setFixedWidth(100)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button, alignment=Qt.AlignRight)
        button_layout.addWidget(load_button, alignment=Qt.AlignRight)
        button_layout.addWidget(execute_button, alignment=Qt.AlignRight)
        sql_layout = QVBoxLayout()
        sql_layout.addWidget(self.stmt_text, alignment=Qt.AlignCenter)
        sql_layout.addLayout(button_layout)
        sql_group.setLayout(sql_layout)
        sql_group.setFixedWidth(884)

        main_layout = QVBoxLayout()
        main_layout.addWidget(sql_group, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

        save_button.clicked.connect(self.save_sql)
        load_button.clicked.connect(self.load_sql)
        execute_button.clicked.connect(self.execute_stmt)

    def execute_stmt(self):
        c = self.conn.cursor()
        for stmt in self.stmt_text.toPlainText().rstrip(';').split(';'):
            try:
                c.execute(stmt.strip('\n') + ';')
            except sqlite3.OperationalError as error:
                QMessageBox().warning(self, 'Error', f'{error}', QMessageBox.Close)
        c.close()
        return self.conn.commit()

    def save_sql(self):
        file_path: str = QFileDialog.getSaveFileName(self.parent(), 'Save SQL Statement', self.path, 'SQL File(*.sql)',
                                                     options=QFileDialog.DontConfirmOverwrite)[0]
        if file_path:
            self.path = '/'.join(file_path.split('/')[:-1])
            file = open(file_path, 'w')
            file.write(self.stmt_text.toPlainText())
            file.close()

    def load_sql(self):
        file_path: str = QFileDialog.getOpenFileName(self.parent(), 'Load SQL Statement', self.path, 'SQL File(*.sql)',
                                                     options=QFileDialog.DontConfirmOverwrite)[0]
        if file_path:
            self.path = '/'.join(file_path.split('/')[:-1])
            file = open(file_path, 'r')
            self.stmt_text.setText(''.join(file.readlines()))
            file.close()
