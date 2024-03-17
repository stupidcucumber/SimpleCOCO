from typing import Callable
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
      QPushButton, 
      QWidget,
      QMainWindow,
      QVBoxLayout,
      QLabel
)
from PyQt6.QtGui import (
     QImage
)
from .image import AnnotationImageIcon


def create_button(parent: QWidget, text: str, slot: Callable | None = None) -> QPushButton:
        button = QPushButton(text, parent)
        if slot:
            button.pressed.connect(slot)
        return button


class DatasetPushButton(QPushButton):
    def __init__(self, parent: QMainWindow, name: str, annotator_window: QMainWindow):
        super(DatasetPushButton, self).__init__(parent)
        self._parent = parent
        self.annotator_window = annotator_window
        self.setText(name)
        self.pressed.connect(
             slot=lambda: self.open_annotator()
        )
    
    def open_annotator(self) -> None:
        self.annotator_window.show()
        self._parent.close()


class AnnotationImageButton(QWidget):
    def __init__(self, parent: QWidget, image_id: int, image: QImage,
                 annotations_num: int = 0) -> None:
        super(AnnotationImageButton, self).__init__(parent)
        self.image_icon = AnnotationImageIcon(parent=self, width=200, height=400, image=image)
        self.image_id = image_id
        self.annotations_num = annotations_num
        self._set_layout()

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.image_icon)
        layout.addWidget(QLabel('Image id: %d' % self.image_id, self))
        layout.addWidget(QLabel('Number of annotations: %d' % self.annotations_num, self))
        self.setAutoFillBackground(True)
        self.setLayout(layout)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('AnnotationImageButton:hover{background-color: #606060;}')