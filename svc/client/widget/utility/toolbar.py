from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QToolBar
)
from PyQt6.QtGui import (
    QAction
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