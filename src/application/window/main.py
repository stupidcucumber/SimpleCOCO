from PyQt6.QtWidgets import QMainWindow, QToolBar


class MainWindow(QMainWindow):
    def __init__(self, title: str = 'SimpleCOCO', *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(title)

        toolbar = QToolBar('Toolbar')
        self.addToolBar(toolbar)