# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QFrame, QLabel, QPushButton, \
#     QVBoxLayout, QAction, QHBoxLayout, QLineEdit, QGridLayout

import pymysql
#显示主窗口
# class mainUI(QWidget):
#     # def __init__(self,parent = None):
#     #     super(mainUI,self).__init__(parent)
#     #     self.initUI()  # 界面绘制交给InitUi方法
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()  # 界面绘制交给InitUi方法
#     def initUI(self):
#         self.vbox = QVBoxLayout()
#         self.db = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
#         self.cursor = self.db.cursor()
#         self.mysqlID = 1060
#         sql = '''SELECT * FROM article WHERE id=%d LIMIT 1;''' % self.mysqlID
#         try:
#             # 执行sql语句
#             self.cursor.execute(sql)
#             results = self.cursor.fetchall()
#             for row in results:
#                 title = row[1]
#                 content = row[7]
#         except Exception as e:
#             print(str(e))
#         self.db.close()
#
#         # but = QPushButton("buttontest",self)
#         # but.move(0,0)
#         # but.clicked.connect(quit())
#
#
#         self.resize(800, 600)
#         self.center()
#         self.setWindowTitle('作文评分')
#         # self.show()
#
#     # 控制窗口显示在屏幕中心的方法
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
from main_score import mainUI


class scoreUI(QWidget):
    def __init__(self,parent = None):
        super(scoreUI, self).__init__(parent)
        self.showUI()

    def showUI(self):
        usrName = QLabel("UserName")
        passWd = QLabel("PassWord")
        self.userNameLineEdit = QLineEdit()
        self.passWdLineEdit = QLineEdit()
        self.passWdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usrName, 0, 0, 1, 1)
        gridLayout.addWidget(passWd, 1, 0, 1, 1)
        gridLayout.addWidget(self.userNameLineEdit, 0, 1, 1, 3)
        gridLayout.addWidget(self.passWdLineEdit, 1, 1, 1, 3)

        okPushBtn = QPushButton("登录")
        cancelPushBtn = QPushButton("注册")
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(60)
        btnLayout.addWidget(okPushBtn)
        btnLayout.addWidget(cancelPushBtn)

        okPushBtn.clicked.connect(self.signin)
        cancelPushBtn.clicked.connect(self.regist)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)
        self.setLayout(dlgLayout)
        self.setWindowTitle("Login")
        self.resize(200, 200)
        self.show()

    def signin(self):
        dbuser = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
        userCursor = dbuser.cursor()
        if self.userNameLineEdit.text().strip() == "" or self.passWdLineEdit.text() == "":
            QMessageBox.warning(self,
                                "Warning",
                                "User name or passWord error",
                                QMessageBox.Yes
                                )
            self.userNameLineEdit.clear()
            self.passWdLineEdit.clear()
            self.userNameLineEdit.setFocus()
        else:
            username = self.userNameLineEdit.text().strip()
            passwd = self.passWdLineEdit.text()

            sqlLogIn = 'SELECT * FROM `user` WHERE username="%s" AND passwd="%s";'%(username,passwd)

            try:
                userCursor.execute(sqlLogIn)
                results = userCursor.fetchall()
                if results:
                    self.close()
                    dbuser.close()
                    print('开启主页面')
                    main.show()

                else:
                    QMessageBox.warning(self,
                                        "Warning",
                                        "User name or passWord error",
                                        QMessageBox.Yes
                                        )
                    self.userNameLineEdit.clear()
                    self.passWdLineEdit.clear()
                    self.userNameLineEdit.setFocus()
            except:
                print("数据库查询操作失败")

        # dbuser.close()
    def regist(self):
        print('注册成功')
        ex.close()
        reg.show()


class register(QWidget):
    def __init__(self):
        super().__init__()
        self.showUI()

    def showUI(self):

        usrName = QLabel("UserName")
        passWd = QLabel("PassWord")
        self.userName = QLineEdit()
        self.passWd = QLineEdit()

        gridLayout = QGridLayout()
        gridLayout.addWidget(usrName, 0, 0, 1, 1)
        gridLayout.addWidget(passWd, 1, 0, 1, 1)
        gridLayout.addWidget(self.userName, 0, 1, 1, 3)
        gridLayout.addWidget(self.passWd, 1, 1, 1, 3)


        saveBtn = QPushButton("保存")
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(saveBtn)

        saveBtn.clicked.connect(self.saveUser)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)
        self.setLayout(dlgLayout)

        self.setWindowTitle("注册")
        self.resize(300, 200)

    def saveUser(self):
        if self.userName.text().strip() == "" or self.passWd.text() == "":
            QMessageBox.warning(self,
                                "Warning",
                                "User name or passWord error",
                                QMessageBox.Yes
                                )
            self.userName.clear()
            self.passWd.clear()
        else:
            insertName = self.userName.text().strip()
            insertPassWd = self.passWd.text()

            dbInsert = pymysql.connect("localhost", "liwei", "0000", "articlescore", charset='utf8')
            insertCursor = dbInsert.cursor()

            sqlInsert = "INSERT INTO `user`(username,passwd) VALUES('%s','%s');" % (insertName,insertPassWd)
            try:
                # 执行sql语句
                insertCursor.execute(sqlInsert)
                # 提交到数据库执行
                dbInsert.commit()
            except:
                print('插入错误')
            self.close()
            # 关闭数据库连接
            dbInsert.close()
            ex.show()


if __name__=="__main__":
    app = QApplication(sys.argv)

    reg = register()
    main = mainUI()
    ex = scoreUI()
    # main.show()

    sys.exit(app.exec_())