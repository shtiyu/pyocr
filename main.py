import sys
from PyQt5.QtWidgets import QApplication
from ocr.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw  = MainWindow()
    sys.exit(app.exec_())