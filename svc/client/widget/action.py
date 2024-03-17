from typing import Callable
from PyQt6.QtWidgets import (
    QWidget
)
from PyQt6.QtGui import (
    QAction
)


def create_action(text: str, parent: QWidget, slot: Callable | None = None) -> None:
    action = QAction(text, parent)
    if slot:
        action.triggered.connect(slot=slot)
    return action