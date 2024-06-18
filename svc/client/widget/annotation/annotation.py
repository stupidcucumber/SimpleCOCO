from PyQt6.QtCore import QObject, QRect
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget
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


class AnnotationWidget(QWidget):
    def __init__(self, annotation: Annotation, image_width: int, image_height: int,
                 parent: QObject | None = None) -> None:
        super(AnnotationWidget, self).__init__(parent)
        self.annotation = annotation
        self.image_width = image_width
        self.image_height = image_height
        self.setGeometry(self._calculate_geometry())
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
        
    def _setup_layout(self) -> None:
        color_hex = color_from_annotation(annotation=self.annotation).name()
        self.setStyleSheet('border: 2px solid %s;' % color_hex)