import itertools
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QLabel
)
from ..button import AnnotationImageButton


class Page(QWidget):
    def __init__(self, parent: QObject, page_index: int, icons: list[AnnotationImageButton], max_columns: int) -> None:
        super(Page, self).__init__(parent)
        self.max_columns = max_columns
        self.page_index = page_index
        self.icons = icons
        self._setup_widget()

    def _batched_icons(self, n: int):
        iterator = iter(self.icons)
        while batch := tuple(itertools.islice(iterator, n)):
            yield batch

    def _setup_widget(self) -> None:
        if self.icons:
            layout = QGridLayout()
            for row_index, batch in enumerate(self._batched_icons(n=self.max_columns)):
                for column_index, icon in enumerate(batch):
                    layout.addWidget(icon, row_index, column_index)
        else:
            layout = QVBoxLayout()
            label = QLabel('No Images', self)
            layout.addWidget(label)
        self.setLayout(layout)
