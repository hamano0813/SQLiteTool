#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat


class SQLiteHighlighter(QSyntaxHighlighter):
    rules = []
    normal_format = QTextCharFormat()
    normal_format.setFont(QFont('Consolas'))
    normal_format.setFontWeight(QFont.Bold)
    normal_format.setFontPointSize(11)

    def __init__(self, parent=None):
        super(SQLiteHighlighter, self).__init__(parent)
        keywords = (
            'ABORT',
            'ACTION',
            'ADD',
            'AFTER',
            'ALL',
            'ALTER',
            'ANALYZE',
            'AND',
            'AS',
            'ASC',
            'ATTACH',
            'AUTOINCREMENT',
            'BEFORE',
            'BEGIN',
            'BETWEEN',
            'BY',
            'CASCADE',
            'CASE',
            'CAST',
            'CHECK',
            'COLLATE',
            'COLUMN',
            'COMMIT',
            'CONFLICT',
            'CONSTRAINT',
            'CREATE',
            'CROSS',
            'CURRENT_DATE',
            'CURRENT_TIME',
            'CURRENT_TIMESTAMP',
            'DATABASE',
            'DEFAULT',
            'DEFERRABLE',
            'DEFERRED',
            'DELETE',
            'DESC',
            'DETACH',
            'DISTINCT',
            'DROP',
            'EACH',
            'ELSE',
            'END',
            'ESCAPE',
            'EXCEPT',
            'EXCLUSIVE',
            'EXISTS',
            'EXPLAIN',
            'FAIL',
            'FOR',
            'FOREIGN',
            'FROM',
            'FULL',
            'GLOB',
            'GROUP',
            'HAVING',
            'IF',
            'IGNORE',
            'IMMEDIATE',
            'IN',
            'INDEX',
            'INDEXED',
            'INITIALLY',
            'INNER',
            'INSERT',
            'INSTEAD',
            'INTERSECT',
            'INTO',
            'IS',
            'ISNULL',
            'JOIN',
            'KEY',
            'LEFT',
            'LIKE',
            'LIMIT',
            'MATCH',
            'NATURAL',
            'NO',
            'NOT',
            'NOTNULL',
            'NULL',
            'OF',
            'OFFSET',
            'ON',
            'OR',
            'ORDER',
            'OUTER',
            'PLAN',
            'PRAGMA',
            'PRIMARY',
            'QUERY',
            'RAISE',
            'RECURSIVE',
            'REFERENCES',
            'REGEXP',
            'REINDEX',
            'RELEASE',
            'RENAME',
            'REPLACE',
            'RESTRICT',
            'RIGHT',
            'ROLLBACK',
            'ROW',
            'SAVEPOINT',
            'SELECT',
            'SET',
            'TABLE',
            'TEMP',
            'TEMPORARY',
            'THEN',
            'TO',
            'TRANSACTION',
            'TRIGGER',
            'UNION',
            'UNIQUE',
            'UPDATE',
            'USING',
            'VACUUM',
            'VALUES',
            'VIEW',
            'VIRTUAL',
            'WHEN',
            'WHERE',
            'WITH',
            'WITHOUT'
        )
        functions = (
            'abs',
            'changes',
            'char',
            'coalesce',
            'glob',
            'hex',
            'ifnull',
            'instr',
            'last_insert_rowid',
            'length',
            'like',
            'likelihood',
            'likely',
            'load_extension',
            'lower',
            'ltrim',
            'max',
            'min',
            'nullif',
            'printf',
            'quote',
            'random',
            'randomblob',
            'replace',
            'round',
            'rtrim',
            'soundex',
            'sqlite_compileoption_get',
            'sqlite_compileoption_used',
            'sqlite_offset',
            'sqlite_source_id',
            'sqlite_version',
            'substr',
            'total_changes',
            'trim',
            'trim',
            'typeof',
            'unicode',
            'unlikely',
            'upper',
            'zeroblob',
            'date',
            'time',
            'datetime',
            'julianday',
            'strftime',
            'avg',
            'count',
            'group_concat',
            'sum',
            'total'
        )
        typenames = (
            'INT',
            'INTEGER',
            'TEXT',
            'BLOB',
            'REAL',
            'FLOAT',
            'NUMERIC',
            'BOOLEAN',
            'DATE',
            'DATETIME'
        )

        keyword_format = QTextCharFormat(self.normal_format)
        keyword_format.setForeground(Qt.blue)
        keyword_format.setFontWeight(QFont.ExtraBold)
        function_format = QTextCharFormat(self.normal_format)
        function_format.setForeground(Qt.darkGreen)
        comment_format = QTextCharFormat(self.normal_format)
        comment_format.setForeground(Qt.gray)
        comment_format.setFontItalic(True)
        name_format = QTextCharFormat(self.normal_format)
        name_format.setForeground(Qt.red)
        typename_format = QTextCharFormat(self.normal_format)
        typename_format.setForeground(Qt.magenta)
        typename_format.setFontWeight(QFont.ExtraBold)

        self.rules.append((QRegExp('\\[(\\w|\\W|[\\u4e00-\\u9fa5])*\\]'), name_format))
        self.rules.extend([(QRegExp(f'\\b{pattern}\\b', Qt.CaseInsensitive), typename_format) for pattern in typenames])
        self.rules.extend([(QRegExp(f'\\b{pattern}\\b', Qt.CaseInsensitive), keyword_format) for pattern in keywords])
        self.rules.extend([(QRegExp(f'\\b{pattern}\\b', Qt.CaseInsensitive), function_format) for pattern in functions])
        self.rules.append((QRegExp('--(\\w|\\W|[\\u4e00-\\u9fa5])*$', Qt.CaseInsensitive), comment_format))

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.normal_format)
        for pattern, format_name in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format_name)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
