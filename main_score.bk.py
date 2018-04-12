# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import *

import pymysql
#显示主窗口
from PyQt5.uic.properties import QtGui

from svm import score_result


class mainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initDB()
        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        self.hMainBox = QHBoxLayout()  #主界面水平窗口

        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(65,65,65))
        self.setPalette(palette1)

        self.vButtonBox = QVBoxLayout() #左侧按钮
        self.vMainBox = QVBoxLayout() #作文查看界面作文垂直窗口
        self.hButtonBox = QHBoxLayout()#上一篇下一篇点击事件
        self.vDisplayBox = QVBoxLayout()#作文查看右侧结果显示

        self.vMainInputBox = QVBoxLayout()#作文评分输入
        self.vAssessButtonBox = QHBoxLayout()#作文评分提交结果
        self.vInputResult = QVBoxLayout()#导入作文评分结果
        self.gridInput = QGridLayout()#作文评分输入框

        #作文查看结果显示
        self.lblScore = QLabel("文章等级为："+str(self.score))
        self.lblCount = QLabel("文章字数为："+str(self.count))
        self.lblPragraph = QLabel("文章段落为："+str(self.paragraph))
        self.lblPoem = QLabel("引用古诗数为："+str(self.poem))
        self.lblIdiom = QLabel("引用成语数为：" + str(self.idiom))
        self.lblName = QLabel("引用人名数为："+str(self.name))
        self.lblDictum = QLabel("引用名言数为：" + str(self.dictum))
        #作文查看结果添加
        # self.vDisplayBox.addStretch(1)
        self.vDisplayBox.addWidget(self.lblScore)
        self.vDisplayBox.addWidget(self.lblCount)
        self.vDisplayBox.addWidget(self.lblPragraph)
        self.vDisplayBox.addWidget(self.lblPoem)
        self.vDisplayBox.addWidget(self.lblIdiom)
        self.vDisplayBox.addWidget(self.lblName)
        self.vDisplayBox.addWidget(self.lblDictum)

        #作文评分输入
        self.input = QTextEdit()

        self.lblinput = QLabel("请输入作文：", self)
        self.lblinput.setFont(QFont("Roman times", 20, QFont.Bold))
        self.gridInput.addWidget(self.lblinput, 1, 1, 1, 1)
        self.gridInput.addWidget(self.input, 2, 1, 5, 1)
        self.btImport = QPushButton("本地导入", self)
        self.btImport.clicked.connect(self.importEssay)
        self.btAssess = QPushButton("评价", self)
        self.btAssess.clicked.connect(self.result)
        self.btClear = QPushButton("清空",self)
        self.btClear.clicked.connect(self.clearEssay)
        #作文评分添加
        self.vAssessButtonBox.addStretch(1)
        self.vAssessButtonBox.addWidget(self.btClear)
        self.vAssessButtonBox.addWidget(self.btImport)
        self.vAssessButtonBox.addStretch(6)
        self.vAssessButtonBox.addWidget(self.btAssess)
        self.vMainInputBox.addLayout(self.gridInput)
        self.vMainInputBox.addLayout(self.vAssessButtonBox)

        #作文评分结果
        self.lblInputScore = QLabel("文章等级为：0", self)
        self.lblInputCount = QLabel("文章等级为：0", self)
        self.lblInputPragraph = QLabel("文章段落数：0", self)
        self.lblInputIdiom = QLabel("引用成语数：0", self)
        self.lblInputDictum = QLabel("引用名言数：0", self)
        self.lblInputPoem = QLabel("引用诗词数：0", self)
        self.lblInputName = QLabel("引用人名数：0", self)
        #作文评分结果添加
        self.vInputResult.addWidget(self.lblInputScore)
        self.vInputResult.addWidget(self.lblInputPragraph)
        self.vInputResult.addWidget(self.lblInputCount)
        self.vInputResult.addWidget(self.lblInputPoem)
        self.vInputResult.addWidget(self.lblInputDictum)
        self.vInputResult.addWidget(self.lblInputIdiom)
        self.vInputResult.addWidget(self.lblInputName)

        #主页面左侧按钮
        self.btn1 = QPushButton("作文查看", self)
        self.btn1.setStyleSheet('font-size : 20px')
        self.btn1.clicked.connect(self.essayShow)
        self.btn1.setEnabled(False)

        self.btn2 = QPushButton("作文评分", self)
        self.btn2.setStyleSheet('font-size : 20px')
        self.btn2.clicked.connect(self.assess)

        self.btn3 = QPushButton("退出", self)
        self.btn3.setStyleSheet('font-size : 20px')
        self.btn3.clicked.connect(quit)
        self.vButtonBox.addWidget(self.btn1)
        self.vButtonBox.addWidget(self.btn2)
        self.vButtonBox.addWidget(self.btn3)
        self.vButtonBox.addStretch(1)
        #作文查看显示
        self.lblTitle = QLabel("标题",self)
        self.lblTitle.setText(self.title)
        self.lblTitle.setAlignment(Qt.AlignCenter)
        self.lblTitle.setFont(QFont("Roman times", 20, QFont.Bold))
        # self.lblTitle.setStyleSheet("background-color:red")
        self.lblTitle.setFixedWidth(800)
        # self.lblTitle.resize(600,100)
        self.lblTitle.setMargin(20)
        self.lblTitle.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.lblContent = QLabel("内容",self)
        self.lblContent.setText("        "+self.content)
        self.lblContent.setFont(QFont("Roman times", 11))
        # self.lblContent.setStyleSheet("background-color:green")
        self.lblContent.setFixedWidth(800)
        self.lblContent.setFixedHeight(500)
        self.lblContent.adjustSize()
        self.lblContent.setWordWrap(True)


        #上一篇下一篇点击事件
        self.btPer = QPushButton("上一篇",self)
        self.btPer.clicked.connect(self.clickPer)
        self.btPer.setStyleSheet("background-color:#606060;color: white;border-radius:10px;"
                                 "border:5px groove gray;border-style: outset;")

        self.btNext = QPushButton("下一篇",self)
        self.btNext.clicked.connect(self.clickNext)
        self.btNext.setStyleSheet("background-color:#606060;color: white;border-radius:10px;"
                                 "border:5px groove gray;border-style: outset;")

        self.hButtonBox.setSpacing(80)
        self.hButtonBox.addWidget(self.btPer)
        self.hButtonBox.addStretch(1)
        self.hButtonBox.addWidget(self.btNext)
        self.hButtonBox.setSpacing(80)

        if self.mysqlID==1060:
            self.btPer.setEnabled(False)

        self.vMainBox.addWidget(self.lblTitle)
        self.vMainBox.addWidget(self.lblContent)
        self.vMainBox.addStretch(1)
        self.vMainBox.addLayout(self.hButtonBox)

        # vButtonBox
        buttonFrame = QFrame()

        bttest = QHBoxLayout()
        bttest.addWidget(self.btn1)
        bttest.addWidget(self.btn2)
        bttest.addWidget(self.btn3)

        buttonFrame.setLayout(bttest)
        # buttonFrame.setFrameStyle(self,"border: 1px solid #FF00FF; border-radius: 5px;")
        buttonFrame.setStyleSheet(".QFrame{border: 1px solid #FF00FF; border-radius: 5px;}")

        self.hMainBox.addWidget(buttonFrame)
        # self.hMainBox.addLayout(self.vButtonBox)
        self.hMainBox.addLayout(self.vMainBox)
        self.hMainBox.addLayout(self.vDisplayBox)
        self.hMainBox.addLayout(self.vMainInputBox)
        self.hMainBox.addLayout(self.vInputResult)

        self.setLayout(self.hMainBox)

        self.lblinput.setVisible(False)
        self.input.setVisible(False)
        self.btImport.setVisible(False)
        self.btAssess.setVisible(False)
        self.btClear.setVisible(False)

        self.lblInputScore.setVisible(False)
        self.lblInputCount.setVisible(False)
        self.lblInputPragraph.setVisible(False)
        self.lblInputIdiom.setVisible(False)
        self.lblInputDictum.setVisible(False)
        self.lblInputPoem.setVisible(False)
        self.lblInputName.setVisible(False)

        self.resize(1000, 650)
        self.center()
        self.setWindowTitle('作文评分系统')


    # 控制窗口显示在屏幕中心的方法
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #点击上一篇
    def clickPer(self):
        self.mysqlID = self.mysqlID-1
        if self.mysqlID==1060:
            self.btPer.setEnabled(False)

        self.db = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
        self.cursor = self.db.cursor()
        sql = '''SELECT * FROM article WHERE id=%d LIMIT 1;''' % self.mysqlID
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                self.title = row[1]
                self.content = row[7]
                self.score = row[4]
                self.count = row[2]
                self.paragraph = row[3]
                self.poem = row[6]
                self.idiom = row[5]
                self.name = row[9]
                self.dictum = row[8]
        except Exception as e:
            print(str(e))
        self.db.close()

        self.lblTitle.setText(self.title)
        self.lblContent.setText("        " + self.content)

        self.lblCount.setText("文章字数为：" + str(self.count))
        self.lblPragraph.setText("文章段落为：" + str(self.paragraph))
        self.lblScore.setText("文章等级为：" + str(self.score))
        self.lblPoem.setText("引用诗词为" + str(self.poem))
        self.lblIdiom.setText("引用成语为：" + str(self.idiom))
        self.lblDictum.setText("引用名言为：" + str(self.dictum))
        self.lblName.setText("引用人名为" + str(self.name))

    #点击下一篇
    def clickNext(self):

        self.mysqlID = self.mysqlID+1
        if self.mysqlID>1060:
            self.btPer.setEnabled(True)

        self.db = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
        self.cursor = self.db.cursor()
        sql = '''SELECT * FROM article WHERE id=%d LIMIT 1;''' % self.mysqlID
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                self.title = row[1]
                self.content = row[7]
                self.score = row[4]
                self.count = row[2]
                self.paragraph=row[3]
                self.poem=row[6]
                self.idiom=row[5]
                self.name=row[9]
                self.dictum=row[8]
        except Exception as e:
            print(str(e))
        self.db.close()

        self.lblTitle.setText(self.title)
        self.lblContent.setText("        "+self.content)

        self.lblCount.setText("文章字数为："+str(self.count))
        self.lblPragraph.setText("文章段落为："+str(self.paragraph))
        self.lblScore.setText("文章等级为："+str(self.score))
        self.lblPoem.setText("引用诗词为"+str(self.poem))
        self.lblIdiom.setText("引用成语为："+str(self.idiom))
        self.lblDictum.setText("引用名言为："+str(self.dictum))
        self.lblName.setText("引用人名为"+str(self.name))

    #查看文章点击事件
    def essayShow(self):
        self.btn2.setEnabled(True)
        self.btn1.setEnabled(False)

        self.lblTitle.setVisible(True)
        self.lblContent.setVisible(True)

        self.lblScore.setVisible(True)
        self.lblCount.setVisible(True)
        self.lblDictum.setVisible(True)
        self.lblPoem.setVisible(True)
        self.lblPragraph.setVisible(True)
        self.lblIdiom.setVisible(True)
        self.lblName.setVisible(True)

        self.btPer.setVisible(True)
        self.btNext.setVisible(True)

        self.lblinput.setVisible(False)
        self.input.setVisible(False)

        self.btImport.setVisible(False)
        self.btAssess.setVisible(False)
        self.btClear.setVisible(False)

        self.lblInputScore.setVisible(False)
        self.lblInputCount.setVisible(False)
        self.lblInputPragraph.setVisible(False)
        self.lblInputPoem.setVisible(False)
        self.lblInputIdiom.setVisible(False)
        self.lblInputDictum.setVisible(False)
        self.lblInputName.setVisible(False)

    #文章评分点击事件
    def assess(self):
        self.btn2.setEnabled(False)
        self.btn1.setEnabled(True)

        # self.lblTitle.hide()
        # self.lblContent.hide()
        self.lblTitle.setVisible(False)
        self.lblContent.setVisible(False)

        # self.lblScore.hide()
        # self.lblCount.hide()
        # self.lblDictum.hide()
        # self.lblPoem.hide()
        # self.lblPragraph.hide()
        # self.lblIdiom.hide()
        # self.lblName.hide()
        self.lblScore.setVisible(False)
        self.lblCount.setVisible(False)
        self.lblDictum.setVisible(False)
        self.lblPoem.setVisible(False)
        self.lblPragraph.setVisible(False)
        self.lblIdiom.setVisible(False)
        self.lblName.setVisible(False)

        # self.btPer.hide()
        # self.btNext.hide()
        self.btPer.setVisible(False)
        self.btNext.setVisible(False)

        self.lblinput.setVisible(True)
        self.input.setVisible(True)

        self.btImport.setVisible(True)
        self.btAssess.setVisible(True)
        self.btClear.setVisible(True)

        self.lblInputScore.setVisible(True)
        self.lblInputCount.setVisible(True)
        self.lblInputPragraph.setVisible(True)
        self.lblInputPoem.setVisible(True)
        self.lblInputIdiom.setVisible(True)
        self.lblInputDictum.setVisible(True)
        self.lblInputName.setVisible(True)

    #评价文章
    def result(self):
        essay_content = self.input.toPlainText()
        res = score_result(essay_content)
        self.lblInputScore.setText("文章等级为："+str(res['score']))
        self.lblInputPragraph.setText("文章段落数："+str(int(res['pragrapg']*10)))
        self.lblInputCount.setText("文章字数为："+str(int(res['count']*1000)))
        self.lblInputPoem.setText("引用诗词数："+str(res['poem']))
        self.lblInputDictum.setText("引用成语数："+str(res['dictum']))
        self.lblInputIdiom.setText("引用诗词数："+str(res['idiom']))
        self.lblInputName.setText("引用人名数："+str(res['name']))

    #本地导入文件评价
    def importEssay(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                # self.textEdit.setText(data)
                print(data)
                self.input.setText(data)
    #清空输入
    def clearEssay(self):
        self.input.setText("")

    #初始化数据库
    def initDB(self):
        self.db = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
        self.cursor = self.db.cursor()
        self.mysqlID = 1060
        sql = '''SELECT * FROM article WHERE id=%d LIMIT 1;''' % self.mysqlID
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                self.title = row[1]
                self.content = row[7]
                self.score = row[4]
                self.count = row[2]
                self.paragraph=row[3]
                self.poem=row[6]
                self.idiom=row[5]
                self.name=row[9]
                self.dictum=row[8]
        except Exception as e:
            print(str(e))
        self.db.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    main = mainUI()
    main.show()
    sys.exit(app.exec_())