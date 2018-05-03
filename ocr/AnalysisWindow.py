from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QGridLayout
from PyQt5.QtGui import QPixmap
import configparser
import requests
import time
import random
import hmac, hashlib, base64, json, binascii

class AnalysisWindow(QWidget):

    def __init__(self, filename, x, y):
        super().__init__()
        self.file_path = self.get_file_path(filename)
        self.initUI(x, y)

    def initUI(self, x, y):
        '''
        initUI
        :param x: 窗口起始X位置
        :param y: 窗口起始Y位置
        :return:
        '''
        pixmap = QPixmap(self.file_path)
        review = QLabel()
        review.setPixmap(pixmap)

        reviewEdit = QTextEdit('Loading...')

        grid = QGridLayout()
        grid.setSpacing(10)

        #int row, int column,
        grid.addWidget(review, 0, 0, 5, 1)

        # int fromRow, int fromColumn, int rowSpan, int columnSpan
        grid.addWidget(reviewEdit, 0, 1, 5, 1)

        self.reviewEdit = reviewEdit
        self.setLayout(grid)
        self.setGeometry(x, y, pixmap.width() * 2, pixmap.height() * 2)
        self.setWindowTitle('Result')
        self.analysis()

    def authorization(self):
        config = configparser.ConfigParser()
        config.read('ocr/config/global.ini')

        appid     = config.get('recognition', 'appid')
        bucket    = config.get('recognition', 'bucket')
        secretID  = config.get('recognition', 'secretID')
        secretKey = config.get('recognition', 'secretKey')
        randint   = random.randint(0,100)
        current_time = int(time.time())
        expire_time  = current_time + 3600  * 24 * 30
        auth_str     = "a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&u=%s&f="%(appid, bucket, secretID, expire_time, current_time, randint, "0" )

        bin  = hmac.new(secretKey.encode("utf-8"), auth_str.encode("utf-8"), hashlib.sha1)
        s    = bin.hexdigest()
        s    = binascii.unhexlify(s)
        s    = s + auth_str.encode('ascii')

        return base64.b64encode(s).rstrip()

    def analysis(self):

        # 读取配置文件
        config = configparser.ConfigParser()
        config.read('ocr/config/global.ini')

        url   = config.get('recognition', 'url')
        host  = config.get('recognition', 'host')
        appid = config.get('recognition', 'appid')
        auth  = self.authorization()
        image = base64.b64encode(open(self.file_path, 'rb').read()).rstrip().decode('utf-8')

        headers = {'host': host, 'content-type' : 'application/json', 'authorization' : auth}
        payload = {"appid" : appid, "image" : image }

        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            ret = r.json()
            self.reviewEdit.clear()
            for item in ret['data']['items']:
                self.reviewEdit.append(item['itemstring'])
        except requests.exceptions.RequestException as e:
            self.reviewEdit.setText('请求OCR服务异常')

    def get_file_path(self, filename):
        return "ocr_image/%s"%filename

    def act(self):
        self.show()