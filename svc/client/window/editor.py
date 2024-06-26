from PyQt6.QtCore import QObject, Qt, QRect
from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene
)
from PyQt6.QtGui import (
    QImage,
    QMouseEvent,
    QPixmap,
)
from ..utils import Connection
from ...backend.src.structs import (
    GeneratedImage,
    Annotation
)
from ..widget import (
    AnnotationBox
)
from ..request import (
    get_annotations,
    post_annotation,
    update_annotation,
    delete_annotation
)
from ..utils.image import (
    base64tobytes
)
from ..widget.utility import (
    ControllerToolbar
)


class EditorWindow(QMainWindow):
    def __init__(self, connection: Connection, generated_image: GeneratedImage, parent: QObject | None = None) -> None:
        super(EditorWindow, self).__init__(parent)
        self.generated_image = generated_image
        self.connection = connection
        self.image = QImage.fromData(base64tobytes(self.generated_image.imageDataBase64))
        self.controlTollbar = ControllerToolbar(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view = self._create_graphics_view(self.graphics_scene)
        self.annotations: list[Annotation] = []
        self.annotation_bboxes: list[AnnotationBox] = []
        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.controlTollbar)
        self._setup_layout()

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        left_top_corner_x = a0.pos().x()
        left_top_corner_y = a0.pos().y()
        annotation = Annotation(
            imageId=self.generated_image.imageId,
            classId=self.annotations[0].classId if len(self.annotations) > 0 else 1,
            cxNorm=left_top_corner_x / self.image.width(),
            cyNorm=left_top_corner_y / self.image.height(),
            wNorm=100 / self.image.width(),
            hNorm=100 / self.image.height()
        )
        self.current_annotation_bbox = AnnotationBox(
            color=Qt.GlobalColor.red,
            geometry=self._calculate_rect(annotation=annotation, width=self.image.width(), height=self.image.height()),
            annotation=annotation,
            slot=self.remove_annotation_bbox
        )
        self.annotations.append(annotation)
        self.annotation_bboxes.append(self.current_annotation_bbox)
        self.graphics_scene.addItem(self.current_annotation_bbox)
        post_annotation(
            url=self.connection.build_url(),
            annotation=annotation
        )
        self._setup_layout()
        return super().mousePressEvent(a0)
        
    def remove_annotation_bbox(self, annotation_bbox: AnnotationBox) -> None:
        self.graphics_scene.removeItem(annotation_bbox)
        self.annotations.remove(annotation_bbox.annotation)
        self.annotation_bboxes.remove(annotation_bbox)
        delete_annotation(url=self.connection.build_url(), annotation=annotation_bbox.annotation)
        
    def _create_graphics_view(self, scene: QGraphicsScene) -> QGraphicsView:
        graphics_view = QGraphicsView(scene, self)
        graphics_view.setGeometry(self.geometry())
        return graphics_view
    
    def _calculate_rect(self, annotation: Annotation, width: int, height: int) -> QRect:
        x = int(width * (annotation.cxNorm - 0.5 * annotation.wNorm))
        y = int(height * (annotation.cyNorm - 0.5 * annotation.hNorm))
        w = int(width * annotation.wNorm)
        h = int(height * annotation.hNorm)
        return QRect(x, y, w, h)
    
    def _calculate_annotation_norm_bbox(self, rect: QRect) -> list[float]:
        cxNorm = (rect.x() + rect.width() * 0.5) / self.image.width()
        cyNorm = (rect.y() + rect.height() * 0.5) / self.image.height()
        wNorm = rect.width() / self.image.width()
        hNorm = rect.height() / self.image.height()
        return cxNorm, cyNorm, wNorm, hNorm
    
    def closeEvent(self, e) -> bool:
        for annotation_bbox in self.annotation_bboxes:
            annotation = annotation_bbox.annotation
            newBbox = self._calculate_annotation_norm_bbox(annotation_bbox.geometry())
            annotation.cxNorm = newBbox[0]
            annotation.cyNorm = newBbox[1]
            annotation.wNorm = newBbox[2]
            annotation.hNorm = newBbox[3]
            update_annotation(
                url=self.connection.build_url(),
                annotation=annotation
            )
        return super().closeEvent(e)

    def _setup_layout(self) -> None:
        self.annotations: list[Annotation] = get_annotations(
            url=self.connection.build_url(),
            image_id=self.generated_image.imageId
        )
        self.annotation_bboxes: list[AnnotationBox] = [
            AnnotationBox(
                color=Qt.GlobalColor.red,
                geometry=self._calculate_rect(annotation=annotation, width=self.image.width(), height=self.image.height()),
                annotation=annotation,
                slot=self.remove_annotation_bbox
            ) for annotation in self.annotations
        ]
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(QPixmap(self.image))
        for bbox in self.annotation_bboxes:
            self.graphics_scene.addItem(bbox)
        self.setCentralWidget(self.graphics_view)
        