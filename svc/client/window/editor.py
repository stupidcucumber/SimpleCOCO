from PyQt6.QtCore import QObject, Qt, QRect
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGraphicsView,
    QGraphicsScene
)
from PyQt6.QtGui import (
    QImage,
    QPixmap,
)
from ..utils import Connection
from ...backend.src.structs import (
    GeneratedImage,
    Annotation
)
from ..widget import (
    BoundingBox
)
from ..request import (
    get_annotations
)
from ..utils.image import (
    base64tobytes
)
from ..widget.utility import (
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
        self.annotation_bbox: list[BoundingBox] = [
            BoundingBox() for annotation in self.annotations
        ]
        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self.graphics_scene = self._create_graphics_scene(self.image)
        self.graphics_view = self._create_graphics_view(self.graphics_scene)
        self._setup_layout()
        
    def _create_graphics_scene(self, image: QImage) -> QGraphicsScene:
        graphics_scene = QGraphicsScene(self)
        graphics_scene.addPixmap(QPixmap(image))
        return graphics_scene
        
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

    def _setup_layout(self) -> None:
        for bbox in self.annotation_bbox:
            self.graphics_scene.addItem(bbox)
        self.setCentralWidget(self.graphics_view)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.controlTollbar)