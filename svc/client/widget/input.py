from typing import Callable
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit
)


def create_line_edit(parent: QWidget, slot: Callable | None = None, text: str | None = None, 
                          filler: str | None = None) -> QLineEdit:
    line_edit = QLineEdit(parent)
    line_edit.setText(text)
    line_edit.setPlaceholderText(filler)
    if slot:
        line_edit.textChanged.connect(slot)
    return line_edit