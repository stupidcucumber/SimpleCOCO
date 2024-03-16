import sys
from PyQt6.QtWidgets import QApplication
from svc.client.window import EntryWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EntryWindow()
    window.show()
    app.exec()