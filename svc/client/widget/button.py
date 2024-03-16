from typing import Callable
from PyQt6.QtWidgets import (
      QPushButton, 
      QWidget
)


def create_button(parent: QWidget, text: str, slot: Callable | None = None) -> QPushButton:
        button = QPushButton(text, parent)
        if slot:
            button.pressed.connect(slot)
        return button