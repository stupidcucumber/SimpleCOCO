from PyQt6.QtWidgets import (
    QMainWindow
)


class AnnotatorWindow(QMainWindow):
    def __init__(self, dataset: str, host: str, port: str):
        super(AnnotatorWindow, self).__init__()
        self.database = dataset
        self.host = host
        self.port = port
        self._setup_layout()

    def _setup_layout(self) -> None:
        pass