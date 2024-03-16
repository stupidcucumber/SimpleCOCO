from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from ..widget.layout import setup_box
from ..widget.input import create_line_edit
from ..widget.button import create_button
from ..request.dataset import post_dataset


class CreateDataset(QMainWindow):
    def __init__(self, parent_window: QMainWindow, host: str, port: str) -> None:
        super(QMainWindow, self).__init__()
        self.parent_window = parent_window
        self._setup_layout()
        self.host = host
        self.port = port
        self.dataset_name = None

    def set_dataset_name(self, name: str | None = None) -> None:
        self.dataset_name = name

    def add_dataset(self):
        if self.dataset_name:
            url = 'http://%s:%s/fill/dataset' % (self.host, self.port)
            result = post_dataset(url=url, name=self.dataset_name)
            self.parent_window.update()
            self.close()

    def _setup_layout(self) -> None:
        widget = setup_box(
            parent=self,
            layout=QVBoxLayout(),
            widgets=[
                setup_box(
                    parent=self,
                    layout=QHBoxLayout(),
                    widgets=[
                        QLabel('Dataset name:', self), 
                        create_line_edit(
                            parent=self,
                            slot=lambda event: self.set_dataset_name(event),
                            filler='name')
                    ]
                ),
                create_button(
                    parent=self,
                    text='Create dataset',
                    slot=lambda: self.add_dataset()
                )
            ]
        )
        self.setCentralWidget(widget)