from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLabel
)
from ..utils import Connection
from ..widget.utility import setup_box
from ..widget.utility import create_line_edit, create_area_edit
from ..widget.utility import create_button
from ..request.dataset import post_dataset
from ..request.types import get_dataset_types


class CreateDataset(QMainWindow):
    def __init__(self, parent_window: QMainWindow, connection: Connection) -> None:
        super(QMainWindow, self).__init__()
        self.parent_window = parent_window
        self.connection = connection
        self.dataset_name = None
        self.dataset_description = None
        self._setup_layout()

    def set_dataset_name(self, name: str | None = None) -> None:
        self.dataset_name = name

    def set_dataset_description(self, text: str | None = None) -> None:
        self.dataset_description = text

    def add_dataset(self):
        if self.dataset_name and self.dataset_description:
            result = post_dataset(url=self.connection.build_url(), 
                                  name=self.dataset_name,
                                  description=self.dataset_description)
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
                            filler='name'
                        )
                    ]
                ),
                setup_box(
                    parent=self,
                    layout=QHBoxLayout(),
                    widgets=[
                        QLabel('Dataset description:', self),
                        create_area_edit(
                            parent=self,
                            slot=lambda event: self.set_dataset_description(event)
                        )
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