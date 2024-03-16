import pathlib
from PyQt6.QtWidgets import (
    QLabel,
    QWidget
)
from PyQt6.QtGui import (
    QPixmap
)


class AnnotationImageIcon(QLabel):
    def __init__(self, parent: QWidget, width: int, height: int, image_path: pathlib.Path | str) -> None:
        super(AnnotationImageIcon, self).__init__(parent)
        pixmap = QPixmap(str(image_path))
        self.setPixmap(pixmap)
        self.setFixedSize(width, height)