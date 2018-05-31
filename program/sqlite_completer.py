#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QCompleter, QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from program.word_list import keywords, functions, typenames, remove_list


words = []
words.extend([word for word in keywords])
words.extend([word.lower() for word in keywords])
words.extend([word for word in functions])
words.extend([word.upper() for word in functions])
words.extend([word for word in typenames])
words.extend([word.lower() for word in typenames])
words = set(words)
[words.remove(i.upper()) for i in remove_list]
[words.remove(i.lower()) for i in remove_list]
words = list(words)
words.sort()


class SQLiteCompleterText(QTextEdit):
    def __init__(self, parent=None):
        super(SQLiteCompleterText, self).__init__(parent)
        self._completer = QCompleter(words)
        self._completer.setWrapAround(False)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.activated.connect(self.insertCompletion)

    def completer(self):
        return self._completer

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, e):
        self._completer.setWidget(self)
        super(SQLiteCompleterText, self).focusInEvent(e)

    def keyPressEvent(self, e):
        if self._completer.popup().isVisible():
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                return

        is_shortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_E & Qt.ControlModifier)
        if not is_shortcut:
            super(SQLiteCompleterText, self).keyPressEvent(e)

        ctrl_or_shift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if ctrl_or_shift and len(e.text()) == 0:
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        has_modifier = (e.modifiers() != Qt.NoModifier) and not ctrl_or_shift
        completion_prefix = self.textUnderCursor()

        if not is_shortcut and (has_modifier or len(e.text()) == 0
                                or len(completion_prefix) < 1 or e.text()[-1] in eow):
            self._completer.popup().hide()
            return

        if completion_prefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completion_prefix)
            self._completer.popup().setCurrentIndex(self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(0) +
                    self._completer.popup().verticalScrollBar().sizeHint().width())
        self._completer.complete(cr)
