import enum
from PyQt6.QtCore import QObject, Qt, QRect
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
    QMouseEvent,
    QPixmap,
    QIcon,
    QCursor,
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


class Tools(enum.IntEnum):
    DEFAULT: int = 0
    BOUNDING_BOX: int = 1


class ControllerToolbar(QToolBar):
    def __init__(self, parent: QObject | None = None) -> None:
        super(ControllerToolbar, self).__init__(parent)
        self.current_tool: Tools = Tools.DEFAULT
        self._setup_layout()
        
    def getCurrentTool(self) -> Tools:
        return self.current_tool
        
    def addWidget(self, widget: QWidget | None) -> QAction | None:
        raise NotImplementedError('Use addPushButton instead. Adding other widgets is not supported!')
        
    def addPushButton(self, push_button: QPushButton) -> QAction | None:
        if not isinstance(push_button, QPushButton):
            raise ValueError('Only QPushButton widgets are supported!')
        return super().addWidget(push_button)
    
    def children(self) -> list[QPushButton]:
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
            self.current_tool = Tools.DEFAULT
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
            self.current_tool = Tools.BOUNDING_BOX
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
        self.image = QImage.fromData(base64tobytes(self.generated_image.imageDataBase64))
        self.controlTollbar = ControllerToolbar(self)
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
        self.current_annotation_widget: AnnotationWidget | None = None
        self.first_X: int | None = None
        self.first_Y: int | None = None
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
                return super().mouseMoveEvent(a0)
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
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap.fromImage(self.image))
        for annotation in self.annotations:
            self._draw_annotation(annotation, self.label)
        self.scrollArea.setWidget(self.label)
        self.setCentralWidget(self.scrollArea)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.controlTollbar)