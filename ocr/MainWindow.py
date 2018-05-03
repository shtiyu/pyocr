
from PyQt5.QtWidgets import (QWidget, QDesktopWidget,  QHBoxLayout,
                             QPushButton, QApplication)
from PyQt5.QtCore import Qt, QTimer
from ocr.ScreenShoot import ScreenShootWindow

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setButton()
        self.resize(200, 150)
        self.center()
        self.setWindowTitle('Center')
        self.pop = ScreenShootWindow()
        self.show()

    def setButton(self):
        btn  = QPushButton('选定识别区域', self)

        # btn.sizeHint()显示默认尺寸
        btn.resize(btn.sizeHint())

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn, alignment=Qt.AlignCenter)
        hbox.addStretch(1)

        btn.clicked.connect(self.new_screen_show)
        self.setLayout(hbox)

    # 弹出全屏窗口用于截图
    def pop_window(self):
        if self.pop is None:
            self.pop = ScreenShootWindow()

        self.pop.imageView.setPixmap(self.preview_screen)
        self.pop.act()


    def new_screen_show(self):
        self.hide()
        QTimer.singleShot(500, self.get_screen_shot)

    def get_screen_shot(self):
        self.preview_screen = QApplication.primaryScreen().grabWindow(0)
        self.pop_window()
        self.show()

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())