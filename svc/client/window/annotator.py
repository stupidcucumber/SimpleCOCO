from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)
from ..widget.page import PageScroller
from ..widget.utility import setup_toolbar
from ..widget.utility import create_action, create_button
from ..widget.utility import setup_box


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
        page_scroller = PageScroller(parent=self, dataset_url='', max_images=10, max_columns=3)
        scroll_area = QScrollArea()
        scroll_area.setWidget(page_scroller)
        self.setCentralWidget(
            setup_box(
                parent=self, layout=QVBoxLayout(),
                widgets=[
                    scroll_area,
                    setup_box(self, layout=QHBoxLayout(),
                        widgets=[
                            create_button(parent=self, text='<< Previous Page'),
                            create_button(parent=self, text='Next Page >>')
                        ]        
                    )
                ]
            )
        )