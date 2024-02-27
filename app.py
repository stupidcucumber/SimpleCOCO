import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from src.application.window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()