#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat


class SQLiteHighlighter(QSyntaxHighlighter):
    rules = []
    normal_fmt = QTextCharFormat()
    normal_fmt.setFont(QFont('Consolas'))
    # normal_fmt.setFontWeight(QFont.Bold)
    normal_fmt.setFontPointSize(11)

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

        kw_fmt = QTextCharFormat(self.normal_fmt)
        kw_fmt.setForeground(Qt.blue)
        kw_fmt.setFontWeight(QFont.Bold)
        func_fmt = QTextCharFormat(self.normal_fmt)
        func_fmt.setForeground(Qt.darkGreen)
        cmt_fmt = QTextCharFormat(self.normal_fmt)
        cmt_fmt.setForeground(Qt.gray)
        cmt_fmt.setFontItalic(True)
        name_fmt = QTextCharFormat(self.normal_fmt)
        name_fmt.setForeground(Qt.red)
        tname_fmt = QTextCharFormat(self.normal_fmt)
        tname_fmt.setForeground(Qt.magenta)
        value_fmt = QTextCharFormat(self.normal_fmt)
        value_fmt.setForeground(Qt.darkBlue)
        text_fmt = QTextCharFormat(self.normal_fmt)
        text_fmt.setForeground(Qt.darkYellow)

        self.rules.append((QRegExp('\\b(\-|\+)?\d+(\.\d+)?\\b'), value_fmt))
        self.rules.append((QRegExp('\\b[a-zA-Z]\\w*\\b'), name_fmt))
        self.rules.extend([(QRegExp(f'\\b{pattern}\\b', Qt.CaseInsensitive), tname_fmt) for pattern in typenames])
        self.rules.extend([(QRegExp(f'\\b{pattern}\\b', Qt.CaseInsensitive), kw_fmt) for pattern in keywords])
        self.rules.extend([(QRegExp(f'\\b{pattern}(?=\\()', Qt.CaseInsensitive), func_fmt) for pattern in functions])
        self.rules.append((QRegExp('''(".*"|'.*')'''), text_fmt))
        self.rules.append((QRegExp('\\[([^\\[\\]]*)\\]'), name_fmt))
        self.rules.append((QRegExp('--(\\w|\\W|[\\u4e00-\\u9fa5])*$', Qt.CaseInsensitive), cmt_fmt))

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.normal_fmt)
        for pattern, format_name in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format_name)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
