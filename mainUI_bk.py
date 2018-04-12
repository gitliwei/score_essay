# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *

import pymysql
#显示主窗口
class mainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initDB()
        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        self.hMainBox = QHBoxLayout()
        self.vMainBox = QVBoxLayout()
        self.vButtonBox = QVBoxLayout()
        self.vDisplayBox = QVBoxLayout()

        self.lblScore = QLabel("文章等级为："+str(self.score))
        self.lblCount = QLabel("文章字数为："+str(self.count))
        self.lblPragraph = QLabel("文章段落为："+str(self.paragraph))
        self.lblPoem = QLabel("引用古诗数为："+str(self.poem))
        self.lblIdiom = QLabel("引用成语数为：" + str(self.idiom))
        self.lblName = QLabel("引用人名数为："+str(self.name))
        self.lblDictum = QLabel("引用名言数为：" + str(self.dictum))

        self.vDisplayBox.addStretch(1)
        self.vDisplayBox.addWidget(self.lblScore)
        self.vDisplayBox.addWidget(self.lblCount)
        self.vDisplayBox.addWidget(self.lblPragraph)
        self.vDisplayBox.addWidget(self.lblPoem)
        self.vDisplayBox.addWidget(self.lblIdiom)
        self.vDisplayBox.addWidget(self.lblName)
        self.vDisplayBox.addWidget(self.lblDictum)
        self.vDisplayBox.addStretch(1)

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

        self.lblTitle = QLabel("标题",self)
        self.lblTitle.setText(self.title)
        self.lblTitle.setAlignment(Qt.AlignCenter)
        self.lblTitle.setFont(QFont("Roman times", 20, QFont.Bold))
        self.lblTitle.setMargin(20)

        self.lblContent = QLabel("内容",self)
        self.lblContent.setText("        "+self.content)
        self.lblContent.setFont(QFont("Roman times", 11))
        self.lblContent.adjustSize()
        self.lblContent.setWordWrap(True)

        self.hButtonBox = QHBoxLayout()

        self.btPer = QPushButton("上一篇",self)
        self.btPer.clicked.connect(self.clickPer)

        self.btNext = QPushButton("下一篇",self)
        self.btNext.clicked.connect(self.clickNext)

        self.hButtonBox.setSpacing(40)
        self.hButtonBox.addWidget(self.btPer)
        # self.hButtonBox.addStretch(1)
        self.hButtonBox.setSpacing(350)
        self.hButtonBox.addWidget(self.btNext)
        self.hButtonBox.setSpacing(40)
        if self.mysqlID==1060:
            # self.btPer.hide()
            self.btPer.setEnabled(False)

        self.vMainBox.addWidget(self.lblTitle)
        self.vMainBox.addWidget(self.lblContent)
        self.vMainBox.addStretch(1)
        self.vMainBox.addLayout(self.hButtonBox)

        self.hMainBox.addLayout(self.vButtonBox)
        self.hMainBox.addLayout(self.vMainBox)
        self.hMainBox.addLayout(self.vDisplayBox)

        self.setLayout(self.hMainBox)


        self.resize(1000, 650)
        self.center()
        self.setWindowTitle('作文评分')


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
        print("查看文章")

        self.lblinput.hide()
        self.lblContent.hide()

        self.btImport.hide()
        self.btAssess.hide()

        self.input.hide()

        self.lblInputScore.hide()
        self.lblInputCount.hide()
        self.lblInputPragraph.hide()
        self.lblInputIdiom.hide()
        self.lblInputDictum.hide()
        self.lblInputPoem.hide()
        self.lblInputName.hide()

        self.lblTitle.setEnabled(True)
        self.lblContent.setEnabled(True)
        self.btPer.setEnabled(True)
        self.btNext.setEnabled(True)

    #文章评分点击事件
    def assess(self):
        self.btn2.setEnabled(False)
        self.btn1.setEnabled(True)

        self.lblTitle.hide()
        self.lblContent.hide()

        self.lblScore.hide()
        self.lblCount.hide()
        self.lblDictum.hide()
        self.lblPoem.hide()
        self.lblPragraph.hide()
        self.lblIdiom.hide()
        self.lblName.hide()

        self.btPer.hide()
        self.btNext.hide()

        self.input = QTextEdit()
        self.lblinput = QLabel("请输入作文：",self)

        self.gridInput = QGridLayout()
        self.gridInput.addWidget(self.lblinput,1,1,1,1)
        self.gridInput.addWidget(self.input,2,1,5,1)

        self.btImport = QPushButton("本地导入",self)
        self.btImport.clicked.connect(self.importEssay)

        self.btAssess = QPushButton("评价",self)
        self.btAssess.clicked.connect(self.result)

        # self.gridInput.addWidget(self.btImport,3,0)
        # self.gridInput.addWidget(self.btAssess,3,3)
        self.vAssessButtonBox = QHBoxLayout()
        self.vAssessButtonBox.addStretch(1)
        self.vAssessButtonBox.addWidget(self.btImport)
        self.vAssessButtonBox.addWidget(self.btAssess)

        self.vMainInputBox = QVBoxLayout()
        self.vMainInputBox.addLayout(self.gridInput)
        self.vMainInputBox.addLayout(self.vAssessButtonBox)


        self.lblInputScore = QLabel("文章等级为：0",self)
        self.lblInputCount = QLabel("文章等级为：0",self)
        self.lblInputPragraph = QLabel("文章段落数：0",self)
        self.lblInputIdiom = QLabel("引用成语数：0",self)
        self.lblInputDictum = QLabel("引用名言数：0",self)
        self.lblInputPoem = QLabel("引用诗词数：0",self)
        self.lblInputName = QLabel("引用人名数：0",self)

        self.vInputResult = QVBoxLayout()
        self.vInputResult.addWidget(self.lblInputScore)
        self.vInputResult.addWidget(self.lblInputPragraph)
        self.vInputResult.addWidget(self.lblInputCount)
        self.vInputResult.addWidget(self.lblInputPoem)
        self.vInputResult.addWidget(self.lblInputDictum)
        self.vInputResult.addWidget(self.lblInputIdiom)
        self.vInputResult.addWidget(self.lblInputName)

        self.hMainBox.addLayout(self.vMainInputBox)
        self.hMainBox.addLayout(self.vInputResult)

    #评价文章
    def result(self):
        essay_content = self.input.toPlainText()
        print (essay_content)

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