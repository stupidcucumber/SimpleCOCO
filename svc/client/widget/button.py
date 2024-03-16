from typing import Callable, overload
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
      QPushButton, 
      QWidget,
      QMainWindow
)
from ..window.annotator import AnnotatorWindow


def create_button(parent: QWidget, text: str, slot: Callable | None = None) -> QPushButton:
        button = QPushButton(text, parent)
        if slot:
            button.pressed.connect(slot)
        return button


class DatasetPushButton(QPushButton):
    def __init__(self, parent: QMainWindow, dataset_id: int, name: str, 
                 host: str, port: str):
        super(DatasetPushButton, self).__init__(parent)
        self._parent = parent
        self.dataset_id = dataset_id
        self.host = host
        self.port = port
        self.setText(name)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if not issubclass(type(self.parent()), QMainWindow):
            TypeError('Parent of this widget can be only an object of subclass of class QMainWindow.')
        annotator = AnnotatorWindow(dataset=self.dataset_id, host=self.host, port=self.port)
        annotator.show()
        self._parent.close()
        