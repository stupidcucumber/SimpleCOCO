from typing import Callable
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
      QWidget,
      QVBoxLayout,
      QLabel
)
from PyQt6.QtGui import (
     QImage,
     QMouseEvent
)
from ..image import AnnotationImageIcon
from ....backend.src.structs import (
    GeneratedImage
)
from ...utils.image import (
    base64tobytes
)


class AnnotationImageButton(QWidget):
    def __init__(self, parent: QWidget, 
                 generated_image: GeneratedImage,
                 slot: Callable[[GeneratedImage], None],
                 annotations_num: int = 0) -> None:
        super(AnnotationImageButton, self).__init__(parent)
        self.generated_image = generated_image
        self.image_icon = AnnotationImageIcon(
            parent=self, 
            width=200,
            height=400, 
            image=QImage.fromData(base64tobytes(self.generated_image.imageDataBase64))
        )
        self.annotations_num = annotations_num
        self.slot = slot
        self._set_layout()
        
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        return self.slot(self.generated_image)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.image_icon)
        layout.addWidget(QLabel('Image id: %d' % self.generated_image.imageId, self))
        layout.addWidget(QLabel('Number of annotations: %d' % self.annotations_num, self))
        self.setAutoFillBackground(True)
        self.setLayout(layout)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('AnnotationImageButton:hover{background-color: #606060;}')