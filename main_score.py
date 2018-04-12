# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtCore import QRect, Qt, QMargins
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import *

import pymysql
#显示主窗口
from PyQt5.uic.properties import QtGui
from svm import score_result


class mainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initDB() #初始化数据库
        self.initBar() #设置菜单栏和地址栏
        self.initWeight() #初始化控件
        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        self.centerWidget = QWidget()
        self.initCenterWeight()
        self.setCentralWidget(self.centerWidget)

        self.resize(1000, 650)
        self.center()
        self.setWindowTitle('作文评分系统')

    def initCenterWeight(self):

        # self.centerWidget.setStyleSheet("background-color:red")
        self.vMainBox = QVBoxLayout()

        self.hMainWeight = QWidget()
        self.hMainBox = QHBoxLayout()

        self.mainButtonWidget = QWidget()
        self.mainButttonBox = QVBoxLayout()

        self.showBoxWidget = QWidget()
        self.showBox = QVBoxLayout()
        self.NPButtonBox = QHBoxLayout()

        self.resultWidget = QWidget()
        self.resultBox = QGridLayout()

        #三个按钮
        self.mainButttonBox.addWidget(self.btn1)
        self.mainButttonBox.addWidget(self.btn2)
        self.mainButttonBox.addWidget(self.btn3)
        self.mainButttonBox.addStretch(1)
        # self.mainButttonBox.setContentsMargins(0,0,0,0)

        self.showBox.addWidget(self.lblTitle)
        self.showBox.addWidget(self.lblContent)
        self.NPButtonBox.addWidget(self.btPer)
        self.NPButtonBox.addStretch(1)
        self.NPButtonBox.addWidget(self.btNext)
        self.showBox.addLayout(self.NPButtonBox)
        # self.showBox.setContentsMargins(0,0,0,0)

        self.resultBox.addWidget(self.lblScore,1,0)
        self.resultBox.addWidget(self.lblPragraph,1,1)
        self.resultBox.addWidget(self.lblCount,1,2)
        self.resultBox.addWidget(self.lblPoem,2,0)
        self.resultBox.addWidget(self.lblIdiom,2,1)
        self.resultBox.addWidget(self.lblDictum,2,2)
        self.resultBox.addWidget(self.lblName,2,3)

        self.resultWidget.setLayout(self.resultBox)

        self.showBoxWidget.setLayout(self.showBox)
        self.mainButtonWidget.setLayout(self.mainButttonBox)
        self.mainButtonWidget.setContentsMargins(0,0,0,0)

        self.hMainBox.addWidget(self.mainButtonWidget)
        self.hMainBox.addWidget(self.showBoxWidget)
        self.hMainBox.setContentsMargins(0,0,0,0)

        self.mainButtonWidget.setStyleSheet(".QWidget{background-color:#656565;};")
        # self.showBoxWidget.setStyleSheet(".QWidget{background-color:#656565;border:5px solid green;};")
        self.mainButtonWidget.setFixedWidth(150)
        self.showBoxWidget.setFixedWidth(850)
        self.showBoxWidget.setContentsMargins(0,0,0,0)
        self.mainButtonWidget.setContentsMargins(0,0,0,0)

        self.hMainBox.addWidget(self.inputWeight)
        self.hMainBox.setContentsMargins(0,0,0,0)
        self.inputWeight.setVisible(False)

        self.hMainWeight.setLayout(self.hMainBox)

        self.vMainBox.addWidget(self.hMainWeight)
        self.vMainBox.addWidget(self.resultWidget)
        self.vMainBox.setContentsMargins(0,0,0,0)

        self.resultWidget.setFixedHeight(70)
        # self.resultWidget.setStyleSheet(".QWidget{background-color:#656565;border:5px solid green;};")

        self.centerWidget.setLayout(self.vMainBox)
        # self.marginMain = QMargins(0,0,0,0)
        self.centerWidget.setContentsMargins(0,0,0,0)


    def initBar(self):

        # localtime = time.asctime(time.localtime(time.time()))
        self.statusBar().showMessage(time.strftime("%Y-%m-%d %H:%M", time.localtime()))

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        # self.statusBar()

        # 创建一个菜单栏
        menubar = self.menuBar()
        # 添加菜单
        fileMenu = menubar.addMenu('&File')
        # 添加事件
        fileMenu.addAction(exitAction)

        fileMenu = menubar.addMenu('&Edit')
        fileMenu = menubar.addMenu('&View')
        fileMenu = menubar.addMenu('&help')

    def initWeight(self):
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

        #作文查看显示
        self.lblTitle = QLabel("标题",self)
        self.lblTitle.setText(self.title)
        self.lblTitle.setAlignment(Qt.AlignCenter)
        self.lblTitle.setFont(QFont("Roman times", 20, QFont.Bold))
        self.lblTitle.setFixedWidth(800)
        # self.lblTitle.resize(600,100)
        self.lblTitle.setMargin(20)
        # self.lblTitle.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.lblContent = QLabel("内容",self)
        self.lblContent.setText("       "+self.content+"")
        self.lblContent.setFont(QFont("Roman times", 11))
        self.lblContent.setFixedWidth(800)
        self.lblContent.setFixedHeight(400)
        self.lblContent.adjustSize()
        self.lblContent.setWordWrap(True)


        #上一篇下一篇点击事件
        self.btPer = QPushButton("上一篇",self)
        self.btPer.clicked.connect(self.clickPer)
        self.btPer.setStyleSheet("background-color:#aac5ff;color: white;border-radius:5px;"
                                 "border:3px groove gray;border-style: outset;")
        self.btPer.setFixedWidth(80)
        self.btPer.setFixedHeight(40)

        self.btNext = QPushButton("下一篇",self)
        self.btNext.clicked.connect(self.clickNext)
        self.btNext.setStyleSheet("background-color:#aac5ff;color: white;border-radius:5px;"
                                 "border:3px groove gray;border-style: outset;")
        self.btNext.setFixedWidth(80)
        self.btNext.setFixedHeight(40)

        # 作文查看结果显示
        self.lblScore = QLabel("文章等级为：" + str(self.score))
        self.lblCount = QLabel("文章字数为：" + str(self.count))
        self.lblPragraph = QLabel("文章段落为：" + str(self.paragraph))
        self.lblPoem = QLabel("引用古诗数为：" + str(self.poem))
        self.lblIdiom = QLabel("引用成语数为：" + str(self.idiom))
        self.lblName = QLabel("引用人名数为：" + str(self.name))
        self.lblDictum = QLabel("引用名言数为：" + str(self.dictum))

        lblFont = QFont()
        lblFont.setPointSize(14)

        self.lblScore.setFont(lblFont)
        self.lblCount.setFont(lblFont)
        self.lblPragraph.setFont(lblFont)
        self.lblPoem.setFont(lblFont)
        self.lblIdiom.setFont(lblFont)
        self.lblDictum.setFont(lblFont)
        self.lblName.setFont(lblFont)


        self.inputWeight = QWidget()
        self.hAssessButtonWeight = QWidget()

        self.input = QTextEdit()
        self.lblinput = QLabel("请输入作文：", self)
        self.lblinput.setFont(QFont("Roman times", 20, QFont.Bold))
        self.gridInput = QGridLayout()  # 作文评分输入框

        self.hAssessButtonBox = QHBoxLayout()  # 作文评分提交结果
        self.btImport = QPushButton("本地导入", self)
        self.btImport.clicked.connect(self.importEssay)
        self.btAssess = QPushButton("评价", self)
        self.btAssess.clicked.connect(self.result)
        self.btClear = QPushButton("清空", self)
        self.btClear.clicked.connect(self.clearEssay)
        self.hAssessButtonBox.addWidget(self.btImport)
        self.hAssessButtonBox.addWidget(self.btClear)
        self.hAssessButtonBox.addStretch(1)
        self.hAssessButtonBox.addWidget(self.btAssess)
        self.hAssessButtonWeight.setLayout(self.hAssessButtonBox)

        self.gridInput.addWidget(self.lblinput, 1, 1, 1, 1)
        self.gridInput.addWidget(self.input, 2, 1, 15, 1)
        self.gridInput.addWidget(self.hAssessButtonWeight, 18, 1, 1, 1)
        self.inputWeight.setLayout(self.gridInput)




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
        self.lblContent.setText("        "+ self.content)

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
        self.inputWeight.setVisible(False)
        self.showBoxWidget.setVisible(True)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)

    #文章评分点击事件
    def assess(self):
        self.inputWeight.setVisible(True)
        self.showBoxWidget.setVisible(False)
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)

    #评价文章
    def result(self):
        essay_content = self.input.toPlainText()
        res = score_result(essay_content)
        self.lblScore.setText("文章等级为："+str(res['score']))
        self.lblPragraph.setText("文章段落数："+str(int(res['pragrapg']*10)))
        self.lblCount.setText("文章字数为："+str(int(res['count']*1000)))
        self.lblPoem.setText("引用诗词数："+str(res['poem']))
        self.lblDictum.setText("引用成语数："+str(res['dictum']))
        self.lblIdiom.setText("引用名言数："+str(res['idiom']))
        self.lblName.setText("引用人名数："+str(res['name']))

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