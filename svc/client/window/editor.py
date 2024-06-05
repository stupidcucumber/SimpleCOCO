from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QLabel,
    QToolBar,
    QPushButton
)
from PyQt6.QtGui import (
    QImage,
    QPixmap,
    QIcon
)
from ..utils import Connection
from ...backend.src.structs import (
    GeneratedImage,
    Annotation
)
from ..widget import AnnotationWidget
from ..request import (
    get_annotations,
    post_annotation,
    update_annotation,
    delete_annotation
)
from ..utils.image import (
    base64tobytes
)


class EditorWindow(QMainWindow):
    def __init__(self, url: Connection, generated_image: GeneratedImage, parent: QObject | None = None) -> None:
        super(EditorWindow, self).__init__(parent)
        self.generated_image = generated_image
        self.image = QImage.fromData(base64tobytes(self.generated_image.imageData))
        self.setGeometry(0, 0, self.image.width(), self.image.height())
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
        self._setup_layout()
        
    def _create_add_annotation_button(self) -> QPushButton:
        button = QPushButton(
            QIcon(
                QPixmap('svc/client/graphics/bounding-box-icon.png')
            ), 
            ''
        )
        return button
    
    def _create_cursor_button(self) -> QPushButton:
        button = QPushButton(
            QIcon(
                QPixmap('svc/client/graphics/cursor-icon.png')
            ),
            ''
        )
        return button

    def _setup_toolbar(self) -> QToolBar:
        toolbar = QToolBar(self)
        toolbar.addWidget(self._create_cursor_button())
        toolbar.addWidget(self._create_add_annotation_button())
        return toolbar

    def _setup_layout(self) -> None:
        self.scrollArea = QScrollArea(self)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap.fromImage(self.image))
        self.scrollArea.setWidget(self.label)
        self.setCentralWidget(self.scrollArea)
        self.toolbar = self._setup_toolbar()
        self.addToolBar(self.toolbar)
