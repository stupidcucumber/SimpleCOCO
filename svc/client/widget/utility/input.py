from typing import Callable
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QLineEdit,
    QTextEdit,
    QPlainTextEdit
)


def create_line_edit(parent: QObject, slot: Callable | None = None, text: str | None = None, 
                          filler: str | None = None) -> QLineEdit:
    line_edit = QLineEdit(parent)
    line_edit.setText(text)
    line_edit.setPlaceholderText(filler)
    if slot:
        line_edit.textChanged.connect(slot)
    return line_edit


def create_area_edit(parent: QObject, slot: Callable | None = None,
                     filler: str | None = None) -> QPlainTextEdit:
    text_edit = QPlainTextEdit(parent)
    text_edit.setPlaceholderText(filler)
    if slot:
        text_edit.textChanged.connect(lambda: slot(text_edit.toPlainText()))
    return text_edit