from typing import Callable
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
      QMainWindow,
      QWidget,
      QVBoxLayout,
      QLabel
)
from ....backend.src.structs import (
    Dataset
)


class DatasetPushButton(QWidget):
    def __init__(self, parent: QMainWindow, dataset: Dataset,
                 slot: Callable[[Dataset], None] = lambda: None):
        super(DatasetPushButton, self).__init__(parent)
        self._parent = parent
        self.dataset = dataset
        self.slot = slot
        self.annotator_window = None
        self._set_layout()

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        name = QLabel(self.dataset.datasetName, self)
        id = QLabel('Dataset ID: %d' % self.dataset.datasetId, self)
        description = QLabel(self.dataset.datasetDescription, self)
        layout.addWidget(name)
        layout.addWidget(id)
        layout.addWidget(description)
        self.setLayout(layout)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('DatasetPushButton:hover{background-color: #606060;}')

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        return self.slot(self.dataset)
        