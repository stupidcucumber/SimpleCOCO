from typing import List
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QLabel,
    QToolBar,
    QPushButton,
    QWidget,
    QApplication
)
from PyQt6.QtGui import (
    QAction,
    QImage,
    QPixmap,
    QIcon,
    QCursor
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


class ControllerToolbar(QToolBar):
    def __init__(self, parent: QObject | None = None) -> None:
        super(ControllerToolbar, self).__init__(parent)
        self._setup_layout()
        
    def addWidget(self, widget: QWidget | None) -> QAction | None:
        raise NotImplementedError('Use addPushButton instead. Adding other widgets is not supported!')
        
    def addPushButton(self, push_button: QPushButton) -> QAction | None:
        if not isinstance(push_button, QPushButton):
            raise ValueError('Only QPushButton widgets are supported!')
        return super().addWidget(push_button)
    
    def children(self) -> List[QPushButton]:
        return super().children()
    
    def _enable_except(self, button: QPushButton) -> None:
        for child in self.children():
            if child != button:
                child.setEnabled(True)
            else:
                child.setDisabled(True)
                
    def _instantiate_cursor_button(self) -> QPushButton:
        button = QPushButton(
            QIcon(
                QPixmap('svc/client/graphics/cursor-icon.png')
            ),
            ''
        )
        button.setDisabled(True)
        def slot():
            QApplication.restoreOverrideCursor()
            self._enable_except(button)
        button.pressed.connect(slot) 
        return button
    
    def _instantiate_bbox_button(self) -> QPushButton:
        icon_path = 'svc/client/graphics/bounding-box-icon.png'
        cursor_pixmap = QPixmap(icon_path)
        cursor_pixmap = cursor_pixmap.scaledToHeight(32)
        button = QPushButton(
            QIcon(
                QPixmap(icon_path)
            ),
            ''
        )
        def slot():
            new_cursor = QCursor(cursor_pixmap)
            QApplication.setOverrideCursor(new_cursor)
            self._enable_except(button)
        button.pressed.connect(slot)
        return button
        
    def _setup_layout(self):
        self.addPushButton(
            self._instantiate_cursor_button()
        )
        self.addPushButton(
            self._instantiate_bbox_button()
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

    def _setup_layout(self) -> None:
        self.scrollArea = QScrollArea(self)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap.fromImage(self.image))
        self.scrollArea.setWidget(self.label)
        self.setCentralWidget(self.scrollArea)
        self.controlTollbar = ControllerToolbar(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.controlTollbar)
