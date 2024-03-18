from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QBoxLayout
)
from PyQt6.QtGui import (
    QImage
)
from .page import Page
from ..image import AnnotationImageIcon
from ..button import AnnotationImageButton


class PageScroller(QWidget):
    def __init__(self, parent: QObject, dataset_url: str, 
                 max_images: int, max_columns: int) -> None:
        super(PageScroller, self).__init__(parent)
        self.dataset_url = dataset_url
        self.current_page = 0
        self.max_images = max_images
        self.max_columns = max_columns
        self._setup_layout()
    
    def _extract_icons(self, page_blob: int = 0) -> list[AnnotationImageIcon]:
        return [
            AnnotationImageButton(
                    parent=self,
                    image_id=0,
                    image=QImage('svc/client/graphics/logo.png')
            ) for _ in range(0)
        ]

    def _instantiate_page(self, page_blob: int = 0) -> Page:
        icons = self._extract_icons(page_blob=page_blob)
        return Page(parent=self, page_index=page_blob, icons=icons, max_columns=self.max_columns)

    def next_page(self) -> None:
        self.current_page += 1
        self._setup_layout()

    def previous_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self._setup_layout()

    def _setup_layout(self) -> None:
        layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        layout.addWidget(
            self._instantiate_page(self.current_page)
        )
        self.setLayout(layout)
