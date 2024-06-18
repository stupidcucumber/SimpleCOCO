from PyQt6.QtCore import QObject, Qt, QRect
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QLabel,
    QWidget,
    QStackedLayout
)
from PyQt6.QtGui import (
    QImage,
    QMouseEvent,
    QPixmap,
    QPen,
    QPainter,
    QColor
)
from ..utils import Connection
from ...backend.src.structs import (
    GeneratedImage,
    Annotation
)
from ..widget import AnnotationWidget
from ..request import (
    get_annotations
)
from ..utils.image import (
    base64tobytes
)
from ..widget.utility import (
    Tools,
    ControllerToolbar
)


class EditorWindow(QMainWindow):
    def __init__(self, url: Connection, generated_image: GeneratedImage, parent: QObject | None = None) -> None:
        super(EditorWindow, self).__init__(parent)
        self.generated_image = generated_image
        self.image = QImage.fromData(base64tobytes(self.generated_image.imageDataBase64))
        self.controlTollbar = ControllerToolbar(self)
        self.annotations: list[Annotation] = get_annotations(
            url=url.build_url(),
            image_id=self.generated_image.imageId
        )
        self.annotation_widgets: list[AnnotationWidget] = [
            AnnotationWidget(
                annotation=annotation,
                image_width=self.image.width(),
                image_height=self.image.height()
            ) for annotation in self.annotations
        ]
        self.current_annotation_widget: AnnotationWidget | None = None
        self.first_X: int | None = None
        self.first_Y: int | None = None
        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self._setup_layout()
        
    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.controlTollbar.getCurrentTool() == Tools.DEFAULT:
            print('Default tool!')
        elif self.controlTollbar.getCurrentTool() == Tools.BOUNDING_BOX:
            if self.current_annotation_widget is None:
                self.current_annotation_widget = AnnotationWidget(
                    annotation=Annotation(
                        imageId=self.generated_image.imageId,
                        classId=0,
                        centerX=0.,
                        centerY=0.,
                        normHeight=0.,
                        normWidth=0.
                    ),
                    image_width=self.image.width(),
                    image_height=self.image.height()
                )
                self.first_X = a0.pos().x()
                self.first_Y = a0.pos().y()
                self.annotations.append(self.current_annotation_widget)
            else:
                current_X = a0.pos().x()
                current_Y = a0.pos().y()
                self.current_annotation_widget.setGeometry(
                    self.first_X,
                    self.first_Y,
                    current_X - self.first_X,
                    current_Y - self.first_Y
                )
                self.current_annotation_widget.update()
        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.current_annotation_widget = None
        self.first_X = None
        self.first_Y = None
        return super().mouseReleaseEvent(a0)
    
    def _calculate_rect(self, annotation: Annotation, width: int, height: int) -> QRect:
        x = int(width * (annotation.cxNorm - 0.5 * annotation.wNorm))
        y = int(height * (annotation.cyNorm - 0.5 * annotation.hNorm))
        w = int(width * annotation.wNorm)
        h = int(height * annotation.hNorm)
        return QRect(x, y, w, h)
    
    def _draw_annotation(self, annotation: Annotation, canvas: QLabel) -> None:
        pixmap = canvas.pixmap()
        painter = QPainter(pixmap)
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("#EB5160"))
        painter.setPen(pen)
        rect = self._calculate_rect(
            annotation=annotation,
            width=pixmap.width(),
            height=pixmap.height()
        )
        painter.drawRect(rect)
        painter.end()
        canvas.setPixmap(pixmap)

    def _setup_layout(self) -> None:
        self.scrollArea = QScrollArea(self)
        widget = QWidget(self)
        layout = QStackedLayout(widget)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap.fromImage(self.image))
        layout.addWidget(self.label)
        for annotation_widget in self.annotation_widgets:
            layout.addWidget(annotation_widget)
        self.scrollArea.setWidget(widget)
        self.setCentralWidget(self.scrollArea)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.controlTollbar)