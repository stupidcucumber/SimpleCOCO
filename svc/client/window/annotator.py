import pathlib
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog
)
from ..widget.page import PageScroller
from ..widget.utility import setup_toolbar
from ..widget.utility import create_action, create_button
from ..widget.utility import setup_box
from ..utils.image import image2base64
from ..request.image import upload_generated_image
from ..utils import Connection
from ...backend.src.structs import (
    Dataset,
    GeneratedImage
)


class AnnotatorWindow(QMainWindow):
    def __init__(self, parent: QWidget, dataset: Dataset, connection: Connection):
        super(AnnotatorWindow, self).__init__(parent)
        self.dataset = dataset
        self.connection = connection
        self._rows = 2
        self._columns = 6
        self._setup_layout()
        self.show()

    def _upload_images(self) -> None:
        directory_name = pathlib.Path(QFileDialog.getExistingDirectory())
        formats = ['.png', '.jpg', '.jpeg']
        image_files = []
        for image_format in formats:
            image_files += list(directory_name.glob('*%s' % image_format))
        for image_path in image_files:
            _ = upload_generated_image(
                url=self.connection.build_url(),
                generated_image=GeneratedImage(
                    imageData=image2base64(image_path),
                    datasetId=self.dataset.datasetId
                )
            )

    def _setup_layout(self) -> None:
        self.setMinimumWidth(1400)
        self.setMinimumHeight(800)
        self.setWindowTitle('Annotator: %s' % self.dataset.datasetName)
        toolbar = setup_toolbar(parent=self,
                                items=[
                                    create_action(text='Upload images', parent=self, slot=self._upload_images),
                                    create_action(text='Export dataset', parent=self),
                                    create_action(text='Dataset Info', parent=self),
                                    create_action(text='Dataset Settings', parent=self)
                                ], 
                                orientation=Qt.Orientation.Horizontal)
        self.addToolBar(toolbar)
        page_scroller = PageScroller(parent=self, connection=self.connection, 
                                     dataset_id=self.dataset.datasetId, 
                                     max_images=20, max_columns=5)
        scroll_area = QScrollArea()
        scroll_area.setWidget(page_scroller)
        self.setCentralWidget(
            setup_box(
                parent=self, layout=QVBoxLayout(),
                widgets=[
                    scroll_area,
                    setup_box(
                        self, 
                        layout=QHBoxLayout(),
                        widgets=[
                            create_button(parent=self, text='<< Previous Page', slot=page_scroller.previous_page),
                            create_button(parent=self, text='Next Page >>', slot=page_scroller.next_page)
                        ]        
                    )
                ]
            )
        )
