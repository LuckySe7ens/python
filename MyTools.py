# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyTool.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import urllib.request
from urllib import parse
import urllib.parse
import json
import random
import hashlib
from playsound import playsound
import wget
import time

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QWidget
transurl = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

timeurl = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'

appver = '5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
u = 'fanyideskweb'

c = 'p09@Bn{h02_BIEe]$P^nG'


class Worker(QObject):

    valueChanged = pyqtSignal(str)  # 值变化信号

    def run(self):
        while 1:
            request = urllib.request.Request(timeurl)
            response = urllib.request.urlopen(request)
            timeStamp = json.loads(response.read().decode('utf-8'))['data']['t']
            self.valueChanged.emit(timeStamp[:10])
            QThread.sleep(1)


class Ui_Form(QWidget):
    def __init__(self, *args, **kwargs):
        super(Ui_Form, self).__init__(*args, **kwargs)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(585, 441)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 221, 121))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(320, 10, 256, 121))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(240, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 160, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(150, 160, 211, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 200, 480, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 230, 160, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(340, 230, 150, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 230, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(70, 300, 211, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(60, 330, 141, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(230, 330, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(330, 330, 160, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 启动线程更新进度条值
        self._thread = QThread(self)
        self._worker = Worker()
        self._worker.moveToThread(self._thread)  # 移动到线程中执行
        self._thread.finished.connect(self._worker.deleteLater)
        self._worker.valueChanged.connect(self.lineEdit.setText)
        self.onStart()

        self.preSetData()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Python小工具"))
        self.pushButton.setText(_translate("Form", "中英互译"))
        self.pushButton.clicked.connect(self.on_translate)
        self.pushButton_2.setText(_translate("Form", "播放"))
        self.pushButton_2.clicked.connect(self.on_playVoice)
        self.label.setText(_translate("Form", "Unix时间戳："))
        self.label_2.setText(_translate("Form", "北京时间转Unix时间戳(yyyy-MM-dd HH:mm:ss)"))
        self.pushButton_3.setText(_translate("Form", "转换"))
        self.pushButton_3.clicked.connect(self.on_bjTime2Unix)
        self.label_3.setText(_translate("Form", "Unix时间戳转北京时间"))
        self.pushButton_4.setText(_translate("Form", "转换"))
        self.pushButton_4.clicked.connect(self.on_unix2BjTime)

    def on_translate(self):
        text = self.textEdit.toPlainText()
        if (text.strip() == ''):
            return
        val = translate(text)
        self.textBrowser.setText(json.loads(val)['translateResult'][0][0]['tgt'])

    def on_playVoice(self):
        playMp3(self.textBrowser.toPlainText())

    def on_bjTime2Unix(self):
        self.lineEdit_3.setText(str(str2TimeStamp(self.lineEdit_2.text())))

    def on_unix2BjTime(self):
        self.lineEdit_5.setText(timeStamp2Str(int(self.lineEdit_4.text())))

    def onStart(self):
        self._thread.start()  # 启动线程
        QTimer.singleShot(1, self._worker.run)

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
            # 强制
            # self._thread.terminate()
        del self._thread
        del self._worker
        super(Ui_Form, self).closeEvent(event)

    def preSetData(self):
        self.lineEdit_2.setText(timeStamp2Str(int(time.time())))
        self.lineEdit_4.setText(str(int(time.time())))

def str2TimeStamp(str):
        timeArray = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

import datetime


def timeStamp2Str(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def playMp3(words):
    if(words.strip()==''):
        return
    url = 'http://tts.youdao.com/fanyivoice?le=eng&keyfrom=speaker-target&word='
    url = url + parse.quote(words)
    mp3File = wget.download(url)
    playsound(mp3File)

#     删除文件
#     os.remove(mp3File)


def translate(content):

    f = str(int(time.time() * 1000)) + str(random.randint(1, 10))
    sign = hashlib.md5((u + content + f + c).encode('utf-8')).hexdigest()
    bv = hashlib.md5(appver.encode('utf-8')).hexdigest()

    data = {}
    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = f
    data['sign'] = sign
    data['ts'] = int(time.time() * 1000)
    data['bv'] = bv
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url=transurl, data=data, method='POST')
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')


if __name__ == "__main__":
    import sys
    # from PyQt5.QtGui import QIcon

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    # widget.setWindowIcon(QIcon('web.png'))#增加icon图标，如果没有图片可以没有这句
    widget.show()

    sys.exit(app.exec_())
