from typing import Callable
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
      QMainWindow,
      QWidget,
      QVBoxLayout,
      QLabel
)


class DatasetPushButton(QWidget):
    def __init__(self, parent: QMainWindow, name: str, description: str, dataset_id: int,
                 slot: Callable = lambda: None):
        super(DatasetPushButton, self).__init__(parent)
        self._parent = parent
        self.name = name
        self.description = description
        self.dataset_id = dataset_id
        self.slot = slot
        self.annotator_window = None
        self._set_layout()

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        name = QLabel(self.name, self)
        id = QLabel('Dataset ID: %d' % self.dataset_id, self)
        description = QLabel(self.description, self)
        layout.addWidget(name)
        layout.addWidget(id)
        layout.addWidget(description)
        self.setLayout(layout)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('DatasetPushButton:hover{background-color: #606060;}')

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        return self.slot(self.dataset_id)
        