from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QWidget
)
from PyQt6.QtGui import QImage
from ..widget.button import AnnotationImageButton
from ..widget.utility import setup_toolbar
from ..widget.utility import create_action


class AnnotatorWindow(QMainWindow):
    def __init__(self, parent: QWidget, dataset_id: int, host: str, port: str):
        super(AnnotatorWindow, self).__init__(parent)
        self.dataset_id = dataset_id
        self.host = host
        self.port = port
        self._rows = 2
        self._columns = 6
        self._setup_layout()
        self.show()

    def _setup_layout(self) -> None:
        self.setMinimumWidth(1400)
        self.setMinimumHeight(800)
        self.setWindowTitle('Annotator: %s' % self.dataset_id)
        toolbar = setup_toolbar(parent=self, items=[
                                    create_action(text='Load images', parent=self),
                                    create_action(text='Export dataset', parent=self),
                                    create_action(text='Dataset Info', parent=self),
                                    create_action(text='Dataset Settings', parent=self)
                                ], 
                                orientation=Qt.Orientation.Horizontal)
        self.addToolBar(toolbar)
        widget = QWidget(self)
        layout = QGridLayout()
        for row in range(self._rows):
            for column in range(self._columns):
                image_block = AnnotationImageButton(
                    parent=self,
                    image_id=0,
                    image=QImage('svc/client/graphics/logo.png')
                )
                layout.addWidget(image_block, row, column)
        widget.setLayout(layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        self.setCentralWidget(scroll_area)