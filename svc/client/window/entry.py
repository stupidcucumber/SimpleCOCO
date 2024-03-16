from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
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
from ..widget import DatasetPushButton
from ..widget.toolbar import setup_toolbar
from ..widget.button import create_button
from ..widget.input import create_line_edit
from ..widget.layout import setup_box
from ..request.dataset import get_dataset_names


class EntryWindow(QMainWindow):
    def __init__(self) -> None:
        super(EntryWindow, self).__init__()
        self.host = '127.0.0.1'
        self.port = '8080'
        self.connected = False
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
        buttons = [DatasetPushButton(self, dataset_id=button[0], name=button[1],
                                     host=self.host, port=self.port) for button in names]
        widget = setup_box(
            self,
            layout=QVBoxLayout(),
            widgets=[
                *buttons,
                create_button(parent=self, text='Create dataset', slot=lambda: self._open_create_dataset_window()),
                create_button(parent=self, text='Disconnect', slot=lambda: self.setCentralWidget(self._create_login_widget()))
            ]
        )
        return widget
    
    def _open_create_dataset_window(self):
        window = CreateDataset(self, host=self.host, port=self.port)
        window.show()

    def _open_annotator_window(self, dataset: str):
        window = AnnotatorWindow(
            dataset=dataset,
            host=self.host,
            port=self.port
        )
        window.show()
        self.close()

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
