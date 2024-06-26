import numpy as np
from PyQt6.QtCore import QObject, QRect
from PyQt6.QtGui import (
    QColor,
    QPixmap,
    QImage
)
from PyQt6.QtWidgets import (
    QLabel,
    QFrame
)
from ....backend.src.structs import (
    Annotation
)


def color_from_annotation(annotation: Annotation) -> QColor:
    class_id = annotation.classId
    channel_value = (class_id * 10) % 256
    channels = [channel_value] * 4
    print(channels)
    return QColor.fromRgb(*channels)


class AnnotationWidget(QLabel):
    def __init__(self, annotation: Annotation, image_width: int, image_height: int,
                 parent: QObject | None = None) -> None:
        super(AnnotationWidget, self).__init__(parent)
        self.annotation = annotation
        self.image_width = image_width
        self.image_height = image_height
        self._setup_layout()

    def _calculate_geometry(self) -> QRect:
        width = int(self.image_width * self.annotation.wNorm)
        height = int(self.image_height * self.annotation.hNorm)
        center_x = self.image_width * self.annotation.cxNorm
        center_y = self.image_height * self.annotation.cyNorm
        corner_x = int(center_x - width / 2)
        corner_y = int(center_y - height / 2)
        return QRect(
            corner_x, corner_y,
            width, height
        )
        
    def _create_transparent_pixmap(self, width: int, height: int) -> QPixmap:
        transparent_image = np.zeros((height, width, 4), dtype=np.uint8)
        image = QImage.fromData(transparent_image.tobytes())
        return QPixmap(image)

    def _setup_layout(self) -> None:
        self.setFrameStyle(QFrame.Shape.Panel)
        self.setLineWidth(2)
        geometry = self._calculate_geometry()
        self.setPixmap(
            self._create_transparent_pixmap(
                width=geometry.width(),
                height=geometry.height()
            )
        )
        self.setGeometry(geometry)
