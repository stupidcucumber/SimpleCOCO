from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
      QWidget,
      QVBoxLayout,
      QLabel
)
from PyQt6.QtGui import (
     QImage
)
from ..image import AnnotationImageIcon


class AnnotationImageButton(QWidget):
    def __init__(self, parent: QWidget, image_id: int,
                 image_name: str,
                 image_type_id: int,
                 image: QImage,
                 annotations_num: int = 0) -> None:
        super(AnnotationImageButton, self).__init__(parent)
        self.image_icon = AnnotationImageIcon(parent=self, width=200, height=400, image=image)
        self.image_id = image_id
        self.image_name = image_name
        self.image_type_id = image_type_id
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