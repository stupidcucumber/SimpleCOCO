import enum
from PyQt6.QtCore import (
    QObject
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QToolBar,
    QPushButton,
    QApplication
)
from PyQt6.QtGui import (
    QAction,
    QIcon,
    QCursor,
    QPixmap
)
from PyQt6.QtCore import Qt


def setup_toolbar(parent: QMainWindow, items: list[QWidget],
                  orientation: Qt.Orientation, title: str = 'toolbar') -> QToolBar:
    toolbar = QToolBar(title, parent)
    for item in items:
        if issubclass(type(item), QAction):
            toolbar.addAction(item)
        elif issubclass(type(item), QWidget):
            toolbar.addWidget(item)
    toolbar.setOrientation(orientation)
    return toolbar


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