from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from ocr.MyQLabel import MyQlabel
from ocr.AnalysisWindow import AnalysisWindow
import time

class ScreenShootWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def grab_screen(self, start, end):
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        width = abs(end[0] - start[0]) // 2
        height = abs(end[1] - start[1]) // 2

        des = QApplication.desktop()
        screen = QApplication.primaryScreen()
        filename = "%s.%s"%(time.time(), 'jpg')
        filepath = "ocr_image/%s" % filename
        if screen:
            pix = screen.grabWindow(des.winId(), x, y, width, height)
            pix.save(filepath, "jpg")

        # TODO 无法关闭/隐藏全屏窗口
        self.hide()
        self.analysis = AnalysisWindow(filename, x, y)
        self.analysis.act()


    def initUI(self):
        myQLabel = MyQlabel()
        myQLabel.setScaledContents(True)
        myQLabel.oksignal.connect(lambda: self.grab_screen(myQLabel.start, myQLabel.end))

        self.imageView = myQLabel
        self.vlayout   = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.addWidget(self.imageView)

        self.setLayout(self.vlayout)

    def act(self):
        # TODO OSX进入全屏后无法关闭
        self.showFullScreen()
        # self.showMaximized()
        # QTimer.singleShot(500, self.set_alpha)

