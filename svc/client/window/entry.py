from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QWidget,
    QLabel,
    QSplitter
)
from PyQt6.QtGui import (
    QAction,
    QPixmap
)
from PyQt6.QtCore import Qt
from .createDataset import CreateDataset
from .annotator import AnnotatorWindow
from ..widget.button import DatasetPushButton
from ..widget.utility import setup_toolbar
from ..widget.utility import create_button
from ..widget.utility import create_line_edit
from ..widget.utility import setup_box
from ..request.dataset import get_dataset_names


class EntryWindow(QMainWindow):
    def __init__(self) -> None:
        super(EntryWindow, self).__init__()
        self.host = '127.0.0.1'
        self.port = '8080'
        self.connected = False
        self.annotator_window = None
        self._setup_layout()

    def set_host(self, new_host: str | None = None) -> None:
        self.host = new_host

    def set_port(self, new_port: str | None = None) -> None:
        self.port = new_port

    def update(self) -> None:
        if self.connected:
            self.setCentralWidget(self._create_datasets_widget())
        else:
            self.setCentralWidget(self._create_login_widget())
        super().update()
    
    def _create_login_widget(self) -> QWidget:
        self.connected = False
        return setup_box(
            self,
            layout=QVBoxLayout(),
            widgets=[
                setup_box(self, layout=QHBoxLayout(), widgets=[
                    QLabel('Host:', self), 
                    create_line_edit(self, self.set_host, text=self.host, filler='0.0.0.0')
                ]),
                setup_box(self, layout=QHBoxLayout(), widgets=[
                    QLabel('Port:', self), 
                    create_line_edit(self, self.set_port, text=self.port, filler='5432')
                ]),
                create_button(self, text='Connect', slot=lambda: self.setCentralWidget(self._create_datasets_widget()))
            ]
        )
    
    def _create_datasets_widget(self) -> QWidget:
        self.connected = True
        url = 'http://%s:%s/extract/datasets' % (self.host, self.port)
        names = get_dataset_names(url=url)
        scrollarea = QScrollArea(self)
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for dataset_id, dataset_name in names:
            button = DatasetPushButton(self, name=dataset_name, slot=self._open_annotator_window,
                                       dataset_id=dataset_id)
            layout.addWidget(button)
        widget.setLayout(layout)
        scrollarea.setWidget(widget)
        widget = setup_box(
            self,
            layout=QVBoxLayout(),
            widgets=[
                scrollarea,
                create_button(parent=self, text='Create dataset', slot=lambda: self._open_create_dataset_window()),
                create_button(parent=self, text='Disconnect', slot=lambda: self.setCentralWidget(self._create_login_widget()))
            ]
        )
        return widget
    
    def _open_create_dataset_window(self):
        window = CreateDataset(self, host=self.host, port=self.port)
        window.show()
    
    def _open_annotator_window(self, dataset_id: int) -> None:
        self.annotator_window = AnnotatorWindow(self, dataset_id=dataset_id, host=self.host, port=self.port)
        self.annotator_window.show()

    def _setup_layout(self) -> None:
        toolbar = setup_toolbar(parent=self,
                                items=[
                                    QAction('Settings', self)
                                ],
                                orientation=Qt.Orientation.Horizontal)
        self.addToolBar(toolbar)
        self.setCentralWidget(self._create_login_widget())
    
    def setCentralWidget(self, widget: QWidget) -> None:
        logo_widget = QLabel(self)
        logo_widget.setPixmap(QPixmap('svc/client/graphics/logo.png'))
        _widget = setup_box(
            self,
            layout=QHBoxLayout(),
            widgets=[
                logo_widget,
                QSplitter(self),
                widget
            ]
        )
        super().setCentralWidget(_widget)
