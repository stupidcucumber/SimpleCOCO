import pathlib
from PyQt6.QtWidgets import (
    QLabel,
    QWidget
)
from PyQt6.QtGui import (
    QPixmap,
    QImage
)


class AnnotationImageIcon(QLabel):
    def __init__(self, parent: QWidget, width: int, height: int, image: QImage) -> None:
        super(AnnotationImageIcon, self).__init__(parent)
        self.setPixmap(QPixmap(image))
        self.setFixedSize(width, height)