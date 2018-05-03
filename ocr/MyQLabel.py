from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

class MyQlabel(QLabel):

    oksignal = pyqtSignal()

    def __init__(self, parent=None):
        super(MyQlabel, self).__init__(parent=parent)
        self.start = (0, 0)
        self.end   = (0, 0)
        self.move  = False # 本次点击鼠标是否有选择区域
        self.final_paint = False # 是否结束截图

    def paintEvent(self, event):
        '''
        给出截图的辅助线
        :param event:
        :return:
        '''
        super().paintEvent(event)
        x = self.start[0]
        y = self.start[1]
        w = self.end[0] - x
        h = self.end[1] - y

        qp  = QPainter(self)
        pen = QPen(Qt.transparent)
        qp.setPen(pen)

        if self.final_paint is False:
            qp.setBrush(QColor(255, 255, 255, 160))


        qp.drawRect(x, y, w, h)

    def mousePressEvent(self, event):

        # 点击左键开始选取截图区域
        if event.button() == Qt.LeftButton:
            self.start = (event.pos().x(), event.pos().y())
            self.move = False
            self.final_paint = False

    def mouseReleaseEvent(self, event):

        # 鼠标左键释放开始截图操作
        if event.button() == Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            self.final_paint = True
            self.update()
            if self.move:
                QTimer.singleShot(500, self.send_emit) # 延时500毫秒执行，防止抓取到遮罩层


    def send_emit(self):
        self.oksignal.emit()

    def mouseMoveEvent(self, event):

        # 鼠标左键按下的同时移动鼠标绘制截图辅助线
        if event.buttons() and Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            self.move = True
            self.update()