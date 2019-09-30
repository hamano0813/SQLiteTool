#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QCompleter, QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from program.word_list import keywords, functions, typenames, remove_list

words = []

for w in (keywords, functions, typenames):
    words.extend(word.lower() for word in w)
    words.extend(word.upper() for word in w)

words = set(words)
[words.remove(i.upper()) for i in remove_list]
[words.remove(i.lower()) for i in remove_list]
words = list(words)
words.sort()


class SQLiteCompleterText(QTextEdit):
    def __init__(self, parent=None):
        super(SQLiteCompleterText, self).__init__(parent)
        self.cp = QCompleter(words)
        self.cp.setWrapAround(False)
        self.cp.setWidget(self)
        self.cp.setCompletionMode(QCompleter.PopupCompletion)
        self.cp.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.cp.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, e):
        self.cp.setWidget(self)
        super(SQLiteCompleterText, self).focusInEvent(e)

    def keyPressEvent(self, e):
        if self.cp.popup().isVisible():
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                return

        is_shortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_E & Qt.ControlModifier)
        if not is_shortcut:
            super(SQLiteCompleterText, self).keyPressEvent(e)

        ctrl_or_shift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if ctrl_or_shift and len(e.text()) == 0:
            return

        eo = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        has_modifier = (e.modifiers() != Qt.NoModifier) and not ctrl_or_shift
        cp = self.textUnderCursor()

        if not is_shortcut and (cp in words or has_modifier or len(e.text()) == 0 or len(cp) < 1 or e.text()[-1] in eo):
            self.cp.popup().hide()
            return

        if cp != self.cp.completionPrefix():
            self.cp.setCompletionPrefix(cp)
            self.cp.popup().setCurrentIndex(self.cp.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.cp.popup().sizeHintForColumn(0) + self.cp.popup().verticalScrollBar().sizeHint().width())
        self.cp.complete(cr)
