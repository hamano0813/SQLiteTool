#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QTabWidget, QLineEdit, QPushButton, QGroupBox, QFileDialog,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from import_widget import ImportFrame
from preview_widget import PreviewFrame
from export_widget import ExportFrame
from operate_widget import OperateFrame
import sqlite3


class MainWindow(QWidget):
    conn: sqlite3.connect = None
    path: str = './'

    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        database_group = QGroupBox('Database Setting')
        self.file_path = QLineEdit()
        self.file_path.setFixedWidth(686)
        self.file_path.setReadOnly(True)
        self.new_button = QPushButton('Load')
        self.new_button.setFixedWidth(100)
        connect_button = QPushButton('&Connect')
        connect_button.setFixedWidth(100)
        connect_button.setCheckable(True)
        database_layout = QHBoxLayout()
        database_layout.addWidget(self.file_path, alignment=Qt.AlignCenter)
        database_layout.addWidget(self.new_button, alignment=Qt.AlignCenter)
        database_layout.addWidget(connect_button, alignment=Qt.AlignCenter)
        database_group.setLayout(database_layout)

        self.tab = QTabWidget()
        self.tab.setFixedWidth(920)
        self.import_frame = ImportFrame()
        self.import_frame.setEnabled(False)
        self.preview_frame = PreviewFrame()
        self.preview_frame.setEnabled(False)
        self.operate_frame = OperateFrame()
        self.operate_frame.setEnabled(False)
        self.export_frame = ExportFrame()
        self.export_frame.setEnabled(False)
        self.tab.addTab(self.import_frame, 'Import Data')
        self.tab.addTab(self.preview_frame, 'Preview Data')
        self.tab.addTab(self.operate_frame, 'Operate Data')
        self.tab.addTab(self.export_frame, 'Export Data')

        main_layout = QVBoxLayout()
        main_layout.addWidget(database_group, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.tab, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.setFixedSize(950, 800)
        self.setWindowTitle('SQLite Tool')
        self.new_button.clicked.connect(self.new_database)
        connect_button.clicked.connect(self.connect_database)

    def new_database(self):
        file_path: str = QFileDialog.getSaveFileName(QFileDialog(), 'Load', self.path,
                                                     'Database File(*.sqlite);;Database File(*.db3);;All File(*)',
                                                     options=QFileDialog.DontConfirmOverwrite)[0]
        if file_path:
            self.file_path.setText(file_path)
            self.path = '/'.join(file_path.split('/')[:-1])

    def connect_database(self):
        if not self.sender().isChecked():
            if self.file_path.text() == 'Database in Memory':
                self.file_path.clear()
            self.sender().setText('&Connect')
            self.import_frame.setEnabled(False)
            self.preview_frame.setEnabled(False)
            self.operate_frame.setEnabled(False)
            self.export_frame.setEnabled(False)
            self.new_button.setEnabled(True)
            self.conn.close()
        else:
            if self.file_path.text():
                self.conn = sqlite3.connect(self.file_path.text())
                self.import_frame.conn = self.conn
                self.preview_frame.conn = self.conn
                self.operate_frame.conn = self.conn
                self.export_frame.conn = self.conn
            else:
                self.conn = sqlite3.connect(':memory:')
                self.file_path.setText('Database in Memory')
                self.import_frame.conn = self.conn
                self.preview_frame.conn = self.conn
                self.operate_frame.conn = self.conn
                self.export_frame.conn = self.conn
            self.sender().setText('&Disconnect')
            self.import_frame.setEnabled(True)
            self.preview_frame.setEnabled(True)
            self.operate_frame.setEnabled(True)
            self.export_frame.setEnabled(True)
            self.new_button.setEnabled(False)

    def closeEvent(self, event):
        if self.import_frame.isEnabled():
            self.conn.execute('VACUUM')
            self.conn.close()
        event.accept()
