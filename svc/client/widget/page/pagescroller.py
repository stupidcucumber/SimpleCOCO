from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QLayout,
    QBoxLayout
)
from PyQt6.QtGui import (
    QImage
)
from .page import Page
from ..image import AnnotationImageIcon
from ..button import AnnotationImageButton
from ...request.image import download_generated_images
from ...utils.image import base64tobytes
from ...utils import Connection


class PageScroller(QWidget):
    def __init__(self, parent: QObject, connection: Connection, dataset_id: str,
                 max_images: int, max_columns: int) -> None:
        super(PageScroller, self).__init__(parent)
        self.connection, self.dataset_id = connection, dataset_id
        self.current_page = 0
        self.max_images = max_images
        self.max_columns = max_columns
        self._setup_layout()

    def _instantiate_image(self, data: bytes) -> QImage:
        image = QImage()
        image.loadFromData(data)
        return image
    
    def _clear_layout(self, layout: QLayout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _extract_icons(self, page_blob: int = 0) -> list[AnnotationImageIcon]:
        images = download_generated_images(
            self.connection.build_url(), 
            self.dataset_id, 
            self.max_images, 
            page_blob
        )
        return [
                AnnotationImageButton(
                    parent=self,
                    image_id=image.imageId,
                    dataset_id=image.datasetId,
                    image=self._instantiate_image(base64tobytes(image.imageData)
                )
            ) for image in images
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
        if not self.layout():
            layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
            layout.addWidget(
                self._instantiate_page(self.current_page)
            )
            self.setLayout(layout)
            return
        
        self._clear_layout(self.layout())
        self.layout().addWidget(
            self._instantiate_page(self.current_page)
        )
        self.update()