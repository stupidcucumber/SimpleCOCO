from PyQt6.QtWidgets import (
      QPushButton,
      QMainWindow
)


class DatasetPushButton(QPushButton):
    def __init__(self, parent: QMainWindow, name: str, annotator_window: QMainWindow):
        super(DatasetPushButton, self).__init__(parent)
        self._parent = parent
        self.annotator_window = annotator_window
        self.setText(name)
        self.pressed.connect(
             slot=lambda: self.open_annotator()
        )
    
    def open_annotator(self) -> None:
        self.annotator_window.show()
        self._parent.close()