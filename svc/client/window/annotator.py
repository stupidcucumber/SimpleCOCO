from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QHBoxLayout
)
from ..widget import AnnotationImageIcon
from ..widget.toolbar import setup_toolbar
from ..widget.layout import setup_box


class AnnotatorWindow(QMainWindow):
    def __init__(self, dataset_id: int, host: str, port: str):
        super(AnnotatorWindow, self).__init__()
        self.dataset_id = dataset_id
        self.host = host
        self.port = port
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.setWindowTitle('Annotator: %s' % self.dataset_id)
        toolbar = setup_toolbar(parent=self, items=[], 
                                orientation=Qt.Orientation.Horizontal)
        self.addToolBar(toolbar)
        widget = setup_box(
            parent=self,
            layout=QHBoxLayout(),
            widgets=[AnnotationImageIcon(self, width=200, height=200,
                                         image_path='svc/client/graphics/logo.png') for i in range(10)]
        )
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(widget)
        self.setCentralWidget(scroll_area)
